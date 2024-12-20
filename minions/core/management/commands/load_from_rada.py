import time
from functools import wraps
import os.path
import json
from zipfile import ZipFile
from io import BytesIO

import requests
from dateutil.parser import parse as dt_parse
from translitua import translitua

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from core.models import (
    Convocation,
    MemberOfParliament,
    Minion,
    MP2Convocation,
    Minion2MP2Convocation,
)


def retry(exceptions, tries=4, delay=3, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = "{}, Retrying in {} seconds...".format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--convocation", type=int, default=9)

    @retry(requests.exceptions.ConnectionError)
    def fetch_dataset(self, convocation):
        data_url = "https://data.rada.gov.ua/ogd/mps/skl{}/mps-data-json.zip".format(
            convocation
        )

        r = requests.get(data_url, stream=True)
        fp = BytesIO(r.content)

        with ZipFile(fp) as zip_arch:
            for fname in zip_arch.namelist():
                if fname.lower().endswith("json"):
                    with zip_arch.open(fname) as fp_raw:
                        data = json.loads(fp_raw.read().decode("utf-8"))
                    break

        return data

    def handle(self, *args, **options):
        data = self.fetch_dataset(options["convocation"])
        mps = {}
        mp_cnt = 0
        minions_cnt = 0
        links_cnt = 0
        minion_links_cnt = 0

        regions = {r["id"]: r["name"] for r in data["regions"]}
        parties = {r["id"]: r["name"] for r in data["parties"]}

        conv, _ = Convocation.objects.get_or_create(number=options["convocation"])

        for row in data["mps"]:
            name = "{} {} {}".format(
                row["surname"] or "", row["firstname"] or "", row["patronymic"] or ""
            ).strip()
            dep_data = {
                "name": name,
                "party": parties[row.get("party_id", 50) or 50],
                "district": regions[row["region_id"]] if row.get("region_id") else "",
                "date_from": dt_parse(row["date_oath"]),
                "date_to": dt_parse(row["resignation_date"])
                if row.get("resignation_date")
                else None,
                "link": "http://itd.rada.gov.ua/mps/info/expage/{}/{}".format(
                    row["id"], options["convocation"] + 1
                )
                if options["convocation"] < 9
                else "http://itd.rada.gov.ua/mps/info/page/{}/".format(row["id"]),
            }

            try:
                mp, created = MemberOfParliament.objects.get_or_create(
                    name__iexact=name,
                    defaults={"link": dep_data["link"], "name": dep_data["name"]},
                )

            except MemberOfParliament.MultipleObjectsReturned:
                mp, created = MemberOfParliament.objects.get_or_create(
                    name__iexact=dep_data["name"],
                    link=dep_data["link"],
                    defaults={"link": dep_data["link"], "name": dep_data["name"]},
                )

            if not mp.img and row.get("photo"):
                resp = requests.get(row["photo"])

                if resp.status_code != 200:
                    print("Cannot download image %s for %s" % (
                        row["photo"],
                        mp.name
                    ))
                else:
                    mp.img.save(
                        translitua(mp.name) + ".jpg", ContentFile(resp.content))
                    mp.save()


            dep, link_created = MP2Convocation.objects.update_or_create(
                convocation=conv,
                mp=mp,
                defaults={
                    "party": dep_data["party"],
                    "district": dep_data["district"],
                    "date_from": dep_data["date_from"],
                    "date_to": dep_data["date_to"],
                },
            )

            if created:
                mp_cnt += 1

            if link_created:
                links_cnt += 1

            for minion_row in row.get("assistants", []) or []:
                minion, created = Minion.objects.get_or_create(
                    name__iexact=minion_row["fullname"],
                    defaults={"name": minion_row["fullname"]},
                )

                try:
                    _, link_created = Minion2MP2Convocation.objects.get_or_create(
                        mp2convocation=dep,
                        minion=minion,
                        paid="На платній основі"
                        if minion_row["type_id"] in [2, 3]
                        else "На громадських засадах",
                    )
                except Minion2MP2Convocation.MultipleObjectsReturned:
                    pass

                if created:
                    print("{};{}".format(minion.name, mp.name))
                    minions_cnt += 1

                if link_created:
                    minion_links_cnt += 1

        print(
            "%s MPs, %s links and %s minions (%s links) has been created"
            % (mp_cnt, links_cnt, minions_cnt, minion_links_cnt)
        )

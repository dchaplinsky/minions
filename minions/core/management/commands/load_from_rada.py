import os.path
import json
import requests
from zipfile import ZipFile
from io import BytesIO
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError

from core.models import (
    Convocation, MemberOfParliament, Minion, MP2Convocation,
    Minion2MP2Convocation)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--convocation', type=int, default=8)

    def fetch_dataset(self, convocation):
        data_url = "http://data.rada.gov.ua/ogd/mps/skl{}/mps-data-json.zip".format(convocation)
        r = requests.get(data_url, stream=True)
        fp = BytesIO(r.content)

        with ZipFile(fp) as zip_arch:
            for fname in zip_arch.namelist():
                if fname.lower().endswith("json"):
                    with zip_arch.open(fname, 'r') as fp_raw:
                        data = json.load(fp_raw)
                    break

        return data



    def handle(self, *args, **options):
        data = self.fetch_dataset(options["convocation"])
        mps = {}
        mp_cnt = 0
        minions_cnt = 0
        links_cnt = 0
        minion_links_cnt = 0

        # # MP2Convocation.objects.filter(
        # #     convocation=options["convocation"]).delete()

        # fname = "core/data/rada%s.tsv" % options["convocation"]

        # if not os.path.exists(fname):
        #     raise CommandError(
        #         "TSV file with parliament members doesn't exists for a given"
        #         " convocation")

        # if not os.path.exists(options["source"]):
        #     raise CommandError(
        #         "TSV file with parliament members minions doesn't exists")

        # with open(fname, "r", encoding="utf-8") as fp:
        #     r = reader(fp, delimiter='\t')

        regions = {
            r["id"]: r["name"] for r in data["regions"]
        }
        parties = {
            r["id"]: r["name"] for r in data["parties"]
        }

        conv, _ = Convocation.objects.get_or_create(
            number=options["convocation"])

        for row in data["mps"]:
            name = "{} {} {}".format(row["surname"] or "", row["firstname"] or "", row["patronymic"] or "").strip()
            dep_data = {
                "name": name,
                "party": parties[row.get("party_id", 50) or 50],
                "district": regions[row["region_id"]] if row.get("region_id") else "",
                "date_from": dt_parse(row["date_oath"]),
                "date_to": dt_parse(row["resignation_date"]) if row.get("resignation_date") else None,
                "link": "http://itd.rada.gov.ua/mps/info/expage/{}/{}".format(row["id"], options["convocation"]),
            }

            try:
                mp, created = MemberOfParliament.objects.get_or_create(
                    name__iexact=name, defaults={
                        "link": dep_data["link"],
                        "name": dep_data["name"]
                    })

            except MemberOfParliament.MultipleObjectsReturned:
                mp, created = MemberOfParliament.objects.get_or_create(
                    name__iexact=dep_data["name"],
                    link=dep_data["link"],
                    defaults={
                        "link": dep_data["link"],
                        "name": dep_data["name"]
                    })

            dep, link_created = MP2Convocation.objects.update_or_create(
                convocation=conv, mp=mp,
                defaults={
                    "party": dep_data["party"],
                    "district": dep_data["district"],
                    "date_from": dep_data["date_from"],
                    "date_to": dep_data["date_to"]
                }
            )

            if created:
                mp_cnt += 1

            if link_created:
                links_cnt += 1

            for minion_row in row["assistants"] or []:
                minion, created = Minion.objects.get_or_create(
                    name__iexact=minion_row["fullname"], defaults={
                        "name": minion_row["fullname"]
                    })

                _, link_created = Minion2MP2Convocation.objects.get_or_create(
                    mp2convocation=dep,
                    minion=minion,
                    paid=minion_row["type_id"] in [2, 3]
                )

                if created:
                    minions_cnt += 1

                if link_created:
                    minion_links_cnt += 1


        print("%s MPs, %s links and %s minions (%s links) has been created" % (
            mp_cnt, links_cnt, minions_cnt, minion_links_cnt))

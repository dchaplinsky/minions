import os.path
from csv import reader
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError

from core.models import (
    Convocation, MemberOfParliament, Minion, MP2Convocation,
    Minion2MP2Convocation)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('convocation', type=int)
        parser.add_argument('source')

    def handle(self, *args, **options):
        mps = {}
        mp_cnt = 0
        minions_cnt = 0
        links_cnt = 0

        # MP2Convocation.objects.filter(
        #     convocation=options["convocation"]).delete()

        fname = "core/data/rada%s.tsv" % options["convocation"]

        if not os.path.exists(fname):
            raise CommandError(
                "TSV file with parliament members doesn't exists for a given"
                " convocation")

        if not os.path.exists(options["source"]):
            raise CommandError(
                "TSV file with parliament members minions doesn't exists")

        with open(fname, "r", encoding="utf-8") as fp:
            r = reader(fp, delimiter='\t')

            for row in r:
                mps[row[0].lower()] = {
                    "name": row[0],
                    "party": row[1],
                    "district": row[2],
                    "date_from": dt_parse(row[3][:10], dayfirst=True),
                    "date_to": dt_parse(row[4][:10], dayfirst=True) if row[4][:10] else None,
                    "link": row[5] if "redlink=1" not in row[5] else "",
                }

        conv, _ = Convocation.objects.get_or_create(
            number=options["convocation"])

        with open(options["source"], "r", encoding="utf-8") as fp:
            r = reader(fp, delimiter='\t')

            dep = None

            for row in r:
                if not any(row):
                    continue

                if not any(row[1:]):
                    try:
                        dep_data = mps[row[0].lower()]
                    except KeyError:
                        raise CommandError(
                            "Information on %s is not found" % row[0])

                    try:
                        mp, created = MemberOfParliament.objects.get_or_create(
                            name__iexact=row[0], defaults={
                                "link": dep_data["link"],
                                "name": row[0]
                            })
                    except MemberOfParliament.MultipleObjectsReturned:
                        mp, created = MemberOfParliament.objects.get_or_create(
                            name__iexact=row[0],
                            link=dep_data["link"],
                            defaults={
                                "link": dep_data["link"],
                                "name": row[0]
                            })

                    dep, link_created = MP2Convocation.objects.update_or_create(
                        convocation=conv, mp=mp,
                        party=dep_data["party"],
                        district=dep_data["district"],
                        date_from=dep_data["date_from"],
                        defaults={
                            "date_to": dep_data["date_to"]
                        }
                    )

                    if created:
                        mp_cnt += 1

                    if link_created:
                        links_cnt += 1
                else:
                    if dep is None:
                        raise CommandError(
                            "Minion %s without MP!" % row[1])

                    minion, created = Minion.objects.get_or_create(
                        name__iexact=row[1], defaults={
                            "name": row[1]
                        })

                    Minion2MP2Convocation.objects.get_or_create(
                        mp2convocation=dep,
                        minion=minion,
                        paid=row[3]
                    )

                    if created:
                        minions_cnt += 1

            print("%s MPs, %s links and %s minions has been created" % (
                mp_cnt, links_cnt, minions_cnt))

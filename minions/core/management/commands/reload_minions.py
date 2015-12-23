import os.path
from csv import reader
from dateutil.parser import parse as dt_parse
from django.core.management.base import BaseCommand, CommandError

from core.models import MemberOfParliament, Convocation


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('convocation', type=int)

    def handle(self, *args, **options):
        mps = {}

        fname = "core/data/rada%s.tsv" % options["convocation"]

        if not os.path.exists(fname):
            raise CommandError(
                "TSV file with parliament members doesn't exists for a given"
                " convocation")


        conv, _ = Convocation.objects.get_or_create(
            number=options["convocation"])


        with open(fname, "r", encoding="utf-8") as fp:
            r = reader(fp, delimiter='\t')

            for row in r:
                mp, _ = MemberOfParliament.objects.update_or_create(
                    name__iexact=row[0], defaults={
                        "link": row[5] if "redlink=1" not in row[5] else "",
                        "name": row[0]
                    })

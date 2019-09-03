import re
from django.core.management.base import BaseCommand, CommandError

from core.models import MemberOfParliament


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mp in MemberOfParliament.objects.all().iterator():
            links = set([mp.link] + list(mp.mp2convocation_set.values_list("link", flat=True)))
            
            ids = set()
            for l in links:
                m = re.search(r"page/(\d+)", l)
                if m:
                    ids |= set([int(m.group(1))])

            if len(ids) != 1:
                continue

            dep_id = list(ids)[0]

            for link in mp.mp2convocation_set.all():
                if link.convocation_id == 9:
                    link.link = "https://itd.rada.gov.ua/mps/info/page/{}".format(dep_id)
                else:
                    link.link = "https://itd.rada.gov.ua/mps/info/expage/{}/{}".format(dep_id, link.convocation_id + 1)

                link.save()
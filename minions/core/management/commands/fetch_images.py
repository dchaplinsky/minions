import os
import requests
from core.models import MP2Convocation
from csv import DictReader
from translitua import translitua
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('convocation', type=int)
        parser.add_argument('source')

    def handle(self, *args, **options):
        if not os.path.exists(options["source"]):
            raise CommandError(
                "CSV file with parliament members photos doesn't exists")

        with open(options["source"], "r", encoding="utf-8") as fp:
            mps = {}
            r = DictReader(fp)

            for row in r:
                mps[row["name.text"].lower()] = {
                    "link": row["name.href"],
                    "img": row["image.src"]
                }


        for mp in MP2Convocation.objects.filter(
                convocation_id=options["convocation"]).select_related("mp"):
            if mp.mp.name.lower() not in mps:
                print("%s not found" % mp.mp.name)
                continue

            data = mps[mp.mp.name.lower()]
            mp.link = data["link"]
            mp.save()

            if not mp.mp.img:
                resp = requests.get(data["img"])

                if resp.status_code != 200:
                    print("Cannot download image %s for %s" % (
                        data["img"],
                        mp.mp.name
                    ))
                    continue

                mp.mp.img.save(
                    translitua(mp.mp.name) + ".jpg", ContentFile(resp.content))
                mp.mp.save()
            else:
                print("Image for %s already exists" % mp.mp.name)                

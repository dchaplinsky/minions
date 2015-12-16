import requests
from bs4 import BeautifulSoup
from core.models import MemberOfParliament
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mp in MemberOfParliament.objects.filter(
            img_retrieved=False, img="").exclude(link=""):

            print(mp.link)
            soup = BeautifulSoup(requests.get(mp.link).text)
            img_src = soup.find('table', class_="infobox").find("img")["src"]

            print(img_src)

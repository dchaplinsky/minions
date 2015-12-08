import re
from string import capwords
from django.db import models
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict


class Convocation(models.Model):
    number = models.IntegerField("Скликання", primary_key=True)
    year_from = models.IntegerField("З", blank=True, null=True)
    year_to = models.IntegerField("По", blank=True, null=True)
    img = models.ImageField(blank=True)

    def __unicode__(self):
        return "%s скликання" % (self.number)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = "Скликання"
        verbose_name_plural = "Скликання"


class MP2Convocation(models.Model):
    party = models.CharField("Партія", max_length=200, blank=True)
    district = models.CharField("Округ", max_length=200, blank=True)

    date_from = models.DateField(blank=True)
    date_to = models.DateField(blank=True)

    mp = models.ForeignKey("MemberOfParliament")
    convocation = models.ForeignKey("Convocation")

    def __unicode__(self):
        return "%s, депутат %s скликання" % (self.mp.name, self.convocation_id)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = "Належність до скликання"
        verbose_name_plural = "Належності до скликання"


class MemberOfParliament(models.Model):
    convocations = models.ManyToManyField(
        "Convocation", verbose_name="Скликання", through="MP2Convocation")
    name = models.CharField("ПІБ", max_length=200)
    link = models.URLField("Посилання", max_length=512, blank=True)

    def __unicode__(self):
        return "Нардеп %s" % (self.name)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse("mp_details", kwargs={"mp_id": self.pk})

    def to_dict(self):
        """
        Convert Minion model to an indexable presentation for ES.
        """
        return model_to_dict(self, fields=[
            "id", "convocation", "name", "party", "link", "district",
            "date_from", "date_to"])

    class Meta:
        verbose_name = "Депутат"
        verbose_name_plural = "Депутати"


def title(s):
    chunks = s.split()
    chunks = map(lambda x: capwords(x, u"-"), chunks)
    return u" ".join(chunks)


def parse_fullname(person_name):
    # Extra care for initials (especialy those without space)
    person_name = re.sub("\s+", " ",
                         person_name.replace(".", ". ").replace('\xa0', " "))

    chunks = person_name.strip().split(" ")

    last_name = ""
    first_name = ""
    patronymic = ""

    if len(chunks) == 2:
        last_name = title(chunks[0])
        first_name = title(chunks[1])
    elif len(chunks) > 2:
        last_name = title(" ".join(chunks[:-2]))
        first_name = title(chunks[-2])
        patronymic = title(chunks[-1])

    return last_name, first_name, patronymic


class Minion(models.Model):
    mp = models.ForeignKey("MP2Convocation", verbose_name="Депутат")
    name = models.CharField("ПІБ", max_length=200)
    paid = models.CharField("Засади", max_length=200)

    def to_dict(self):
        """
        Convert Minion model to an indexable presentation for ES.
        """
        d = model_to_dict(self, fields=["id", "name", "paid"])

        d["mp"] = self.mp.to_dict()

        def generate_suggestions(last_name, first_name, patronymic):
            if not last_name:
                return []

            return [
                " ".join([last_name, first_name, patronymic]),
                " ".join([first_name, patronymic, last_name]),
                " ".join([first_name, last_name])
            ]

        d["name_suggest"] = {
            "input": generate_suggestions(*parse_fullname(self.name)),
            "output": self.name
        }

        d["mp_name_suggest"] = {
            "input": generate_suggestions(*parse_fullname(self.mp.name)),
            "output": self.mp.name
        }

        d["_id"] = d["id"]

        return d

    class Meta:
        verbose_name = "Помічник"
        verbose_name_plural = "Помічники"

    def __unicode__(self):
        return "Помічник %s (%s)" % (self.name, self.mp)

    def __str__(self):
        return self.__unicode__()

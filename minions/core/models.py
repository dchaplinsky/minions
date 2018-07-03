import re
from django.db import models
from django.urls import reverse
from django.forms.models import model_to_dict

from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions
)


class Convocation(models.Model):
    number = models.IntegerField("Скликання", primary_key=True)
    year_from = models.IntegerField("З", blank=True, null=True)
    year_to = models.IntegerField("По", blank=True, null=True)
    img = models.ImageField(blank=True)

    def get_absolute_url(self):
        return reverse("convocation", kwargs={"convocation_id": self.pk})

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
    date_to = models.DateField(blank=True, null=True)
    link = models.URLField("Посилання", max_length=512, blank=True)

    mp = models.ForeignKey("MemberOfParliament", on_delete=models.CASCADE)
    convocation = models.ForeignKey("Convocation", on_delete=models.CASCADE)

    def to_dict(self):
        m = model_to_dict(self, fields=[
            "party", "district", "date_from", "date_to"])

        m["convocation"] = self.convocation_id
        m["name"] = self.mp.name
        m["link"] = self.mp.link
        m["id"] = self.mp.id
        m["grouper"] = "%s %s" % (self.convocation_id, self.mp.name)

        return m

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
    name = models.CharField("ПІБ", max_length=200, db_index=True)
    link = models.URLField("Посилання", max_length=512, blank=True)
    img = models.ImageField(blank=True)
    img_retrieved = models.BooleanField(default=False, db_index=True)


    def __unicode__(self):
        return "Нардеп %s" % (self.name)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse("mp_details", kwargs={"mp_id": self.pk})

    class Meta:
        verbose_name = "Депутат"
        verbose_name_plural = "Депутати"


class Minion2MP2Convocation(models.Model):
    mp2convocation = models.ForeignKey("MP2Convocation", on_delete=models.CASCADE)
    minion = models.ForeignKey("Minion", on_delete=models.CASCADE)
    paid = models.CharField("Засади", max_length=200, db_index=True)

    def to_dict(self):
        """
        Convert Minion model to an indexable presentation for ES.
        """
        all_persons = set()
        names_autocomplete = set()

        d = model_to_dict(self, fields=["paid"])

        d["mp"] = self.mp2convocation.to_dict()

        all_persons |= parse_and_generate(self.mp2convocation.mp.name, "Депутат")
        names_autocomplete |= autocomplete_suggestions(self.mp2convocation.mp.name)


        all_persons |= parse_and_generate(self.minion.name, "Помічник")
        names_autocomplete |= autocomplete_suggestions(self.minion.name)

        d["_id"] = self.id
        d["id"] = self.minion.id
        d["name"] = self.minion.name
        d["companies"] = [self.mp2convocation.party]
        d["persons"] = list(filter(None, all_persons))
        d["names_autocomplete"] = list(names_autocomplete)

        return d

    class Meta:
        verbose_name = "Належність помічника до депутата"
        verbose_name_plural = "Належності помічників до депутатов"


class Minion(models.Model):
    mp = models.ManyToManyField(
        "MP2Convocation", verbose_name="Депутат",
        through=Minion2MP2Convocation)
    name = models.CharField("ПІБ", max_length=200, db_index=True)

    def get_absolute_url(self):
        return reverse("minion_details", kwargs={"minion_id": self.pk})

    class Meta:
        verbose_name = "Помічник"
        verbose_name_plural = "Помічники"

    def __unicode__(self):
        return "Помічник %s (%s)" % (self.name, self.mp)

    def __str__(self):
        return self.__unicode__()

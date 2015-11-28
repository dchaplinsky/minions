from django.db import models


class Convocation(models.Model):
    number = models.IntegerField("Скликання", primary_key=True)
    year_from = models.IntegerField("З", blank=True, null=True)
    year_to = models.IntegerField("По", blank=True, null=True)

    def __unicode__(self):
        return "%s скликання" % (self.number)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = "Скликання"
        verbose_name_plural = "Скликання"


class MemberOfParliament(models.Model):
    convocation = models.ForeignKey("Convocation", verbose_name="Скликання")
    name = models.CharField("ПІБ", max_length=200)
    party = models.CharField("Партія", max_length=200, blank=True)
    link = models.URLField("Посилання", max_length=512, blank=True)
    district = models.CharField("Округ", max_length=200, blank=True)

    date_from = models.DateField(blank=True)
    date_to = models.DateField(blank=True)

    def __unicode__(self):
        return "Нардеп %s" % (self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = "Депутат"
        verbose_name_plural = "Депутати"


class Minion(models.Model):
    mp = models.ForeignKey("MemberOfParliament", verbose_name="Депутат")
    name = models.CharField("ПІБ", max_length=200)
    paid = models.CharField("Засади", max_length=200)

    class Meta:
        verbose_name = "Помічник"
        verbose_name_plural = "Помічники"

    def __unicode__(self):
        return "Помічник %s (%s)" % (self.name, self.mp)

    def __str__(self):
        return self.__unicode__()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import migrations


def drop_erroneous_date_to(apps, schema_editor):
    MP2Convocation = apps.get_model("core", "MP2Convocation")
    MP2Convocation.objects.filter(date_to=datetime.datetime(2015, 12, 12)).update(date_to=None)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20161227_0356'),
    ]

    operations = [
        migrations.RunPython(drop_erroneous_date_to),
    ]

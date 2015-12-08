# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def purge_with_fire(apps, schema_editor):
    MP = apps.get_model("core", "MemberOfParliament")
    MP.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151208_0238'),
    ]

    operations = [
        migrations.RunPython(purge_with_fire),
    ]

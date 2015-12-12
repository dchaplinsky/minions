# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def purge_with_fire(apps, schema_editor):
    MP = apps.get_model("core", "MemberOfParliament")
    Minion = apps.get_model("core", "Minion")
    MP.objects.all().delete()
    Minion.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_auto_20151211_0226'),
    ]

    operations = [
        migrations.RunPython(purge_with_fire, migrations.RunPython.noop),
    ]

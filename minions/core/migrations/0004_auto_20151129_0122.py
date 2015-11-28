# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151129_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion',
            name='paid',
            field=models.CharField(max_length=200, verbose_name='Засади'),
        ),
    ]

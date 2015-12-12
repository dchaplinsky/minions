# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151211_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberofparliament',
            name='name',
            field=models.CharField(verbose_name='ПІБ', db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='minion',
            name='name',
            field=models.CharField(verbose_name='ПІБ', db_index=True, max_length=200),
        ),
    ]

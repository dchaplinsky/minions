# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151129_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocation',
            name='year_from',
            field=models.IntegerField(null=True, verbose_name='З', blank=True),
        ),
        migrations.AlterField(
            model_name='convocation',
            name='year_to',
            field=models.IntegerField(null=True, verbose_name='По', blank=True),
        ),
    ]

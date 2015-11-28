# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocation',
            name='year_from',
            field=models.IntegerField(verbose_name='З', blank=True),
        ),
        migrations.AlterField(
            model_name='convocation',
            name='year_to',
            field=models.IntegerField(verbose_name='По', blank=True),
        ),
    ]

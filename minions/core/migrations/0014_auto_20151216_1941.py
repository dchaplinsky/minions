# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151216_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion2mp2convocation',
            name='paid',
            field=models.CharField(max_length=200, db_index=True, verbose_name='Засади'),
        ),
    ]

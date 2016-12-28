# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_mp2convocation_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mp2convocation',
            name='date_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]

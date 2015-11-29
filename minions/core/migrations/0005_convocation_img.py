# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151129_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='convocation',
            name='img',
            field=models.ImageField(upload_to='', blank=True),
        ),
    ]

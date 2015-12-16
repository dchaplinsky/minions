# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151211_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberofparliament',
            name='img',
            field=models.ImageField(upload_to='', blank=True),
        ),
        migrations.AddField(
            model_name='memberofparliament',
            name='img_retrieved',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151208_0248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mp2convocation',
            name='link',
        ),
        migrations.AddField(
            model_name='memberofparliament',
            name='link',
            field=models.URLField(verbose_name='Посилання', blank=True, max_length=512),
        ),
    ]

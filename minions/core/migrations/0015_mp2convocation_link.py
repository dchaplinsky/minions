# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151216_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp2convocation',
            name='link',
            field=models.URLField(max_length=512, blank=True, verbose_name='Посилання'),
        ),
    ]

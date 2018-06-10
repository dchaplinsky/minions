# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151208_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minion',
            name='mp',
            field=models.ForeignKey(verbose_name='Депутат', to='core.MP2Convocation', on_delete=models.CASCADE),
        ),
    ]

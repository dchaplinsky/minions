# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20151208_0250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Minion2MP2Convocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('paid', models.CharField(max_length=200, verbose_name='Засади')),
            ],
            options={
                'verbose_name': 'Належність помічника до депутата',
                'verbose_name_plural': 'Належності помічників до депутатов',
            },
        ),
        migrations.RemoveField(
            model_name='minion',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='minion',
            name='mp',
        ),
        migrations.AddField(
            model_name='minion2mp2convocation',
            name='minion',
            field=models.ForeignKey(to='core.Minion', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='minion2mp2convocation',
            name='mp2convocation',
            field=models.ForeignKey(to='core.MP2Convocation', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='minion',
            name='mp',
            field=models.ManyToManyField(through='core.Minion2MP2Convocation', verbose_name='Депутат', to='core.MP2Convocation'),
        ),
    ]

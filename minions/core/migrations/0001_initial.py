# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convocation',
            fields=[
                ('number', models.IntegerField(serialize=False, primary_key=True, verbose_name='Скликання')),
                ('year_from', models.IntegerField(verbose_name='З')),
                ('year_to', models.IntegerField(verbose_name='По')),
            ],
            options={
                'verbose_name_plural': 'Скликання',
                'verbose_name': 'Скликання',
            },
        ),
        migrations.CreateModel(
            name='MemberOfParliament',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ПІБ')),
                ('party', models.CharField(max_length=200, blank=True, verbose_name='Партія')),
                ('link', models.URLField(max_length=512, blank=True, verbose_name='Посилання')),
                ('district', models.CharField(max_length=200, blank=True, verbose_name='Округ')),
                ('date_from', models.DateField(blank=True)),
                ('date_to', models.DateField(blank=True)),
                ('convocation', models.ForeignKey(to='core.Convocation', verbose_name='Скликання', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Депутати',
                'verbose_name': 'Депутат',
            },
        ),
        migrations.CreateModel(
            name='Minion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ПІБ')),
                ('paid', models.URLField(verbose_name='Засади')),
                ('mp', models.ForeignKey(to='core.MemberOfParliament', verbose_name='Депутат', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Помічники',
                'verbose_name': 'Помічник',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_convocation_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='MP2Convocation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('party', models.CharField(blank=True, verbose_name='Партія', max_length=200)),
                ('link', models.URLField(blank=True, verbose_name='Посилання', max_length=512)),
                ('district', models.CharField(blank=True, verbose_name='Округ', max_length=200)),
                ('date_from', models.DateField(blank=True)),
                ('date_to', models.DateField(blank=True)),
                ('convocation', models.ForeignKey(to='core.Convocation', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Належності до скликання',
                'verbose_name': 'Належність до скликання',
            },
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='convocation',
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='date_to',
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='district',
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='link',
        ),
        migrations.RemoveField(
            model_name='memberofparliament',
            name='party',
        ),
        migrations.AddField(
            model_name='mp2convocation',
            name='mp',
            field=models.ForeignKey(to='core.MemberOfParliament', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='memberofparliament',
            name='convocations',
            field=models.ManyToManyField(to='core.Convocation', through='core.MP2Convocation', verbose_name='Скликання'),
        ),
    ]

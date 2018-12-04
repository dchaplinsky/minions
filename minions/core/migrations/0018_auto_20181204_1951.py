# Generated by Django 2.0.6 on 2018-12-04 19:51

from django.db import migrations



def replace_wrong_labels(apps, schema_editor):
    MP = apps.get_model("core", "Minion2MP2Convocation")
    MP.objects.filter(paid="True").update(paid="На платній основі")
    MP.objects.filter(paid="False").update(paid="На громадських засадах")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20161227_0428'),
    ]

    operations = [
        migrations.RunPython(replace_wrong_labels, migrations.RunPython.noop),
    ]
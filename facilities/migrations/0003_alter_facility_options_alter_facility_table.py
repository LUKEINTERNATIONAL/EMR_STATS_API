# Generated by Django 4.1.2 on 2022-10-12 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0002_alter_facility_facility_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facility',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='facility',
            table='facility',
        ),
    ]

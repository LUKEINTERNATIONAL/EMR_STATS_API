# Generated by Django 3.2.18 on 2023-04-06 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0011_alter_facility_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='viral_load',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

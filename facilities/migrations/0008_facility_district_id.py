# Generated by Django 4.1.3 on 2023-01-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_alter_facility_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='district_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

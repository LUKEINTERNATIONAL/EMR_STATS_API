# Generated by Django 4.1.2 on 2022-10-13 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_alter_facility_table'),
        ('encounters', '0007_alter_enconters_facility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enconters',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.facility'),
        ),
    ]

# Generated by Django 4.1.6 on 2023-02-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viral_load', '0002_alter_viralload_accession_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viralload',
            name='acknowledgement_date',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='viralload',
            name='acknowledgement_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

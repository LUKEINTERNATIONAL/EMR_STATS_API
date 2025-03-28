# Generated by Django 4.1.6 on 2023-02-15 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viral_load', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viralload',
            name='accession_number',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='viralload',
            name='ordered_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='viralload',
            name='person_id',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='viralload',
            name='released_date',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='viralload',
            name='results',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]

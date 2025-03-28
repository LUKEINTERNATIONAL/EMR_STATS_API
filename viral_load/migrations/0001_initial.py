# Generated by Django 4.1.6 on 2023-02-15 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facilities', '0009_alter_facility_district_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViralLoad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accession_number', models.CharField(max_length=200, unique=True)),
                ('person_id', models.CharField(max_length=200)),
                ('results', models.CharField(blank=True, max_length=200)),
                ('ordered_date', models.CharField(max_length=200)),
                ('released_date', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facilities.facility')),
            ],
            options={
                'db_table': 'viral_load',
                'managed': True,
            },
        ),
    ]

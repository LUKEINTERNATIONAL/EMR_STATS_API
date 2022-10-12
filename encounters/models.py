from django.db import models

# Create your models here.
class Enconters(models.Model):
    facility_id = models.CharField(max_length=100)
    program_name = models.CharField(max_length=100)
    total_encounters = models.CharField(max_length=100)
    encounter_date = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()
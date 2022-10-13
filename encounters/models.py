from django.db import models
from facilities.models import Facility 

# Create your models here.
class Enconters(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    program_name = models.CharField(max_length=100)
    total_encounters = models.CharField(max_length=100)
    encounter_date = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'encounters'

    def __str__(self) -> str:
        return super().__str__()
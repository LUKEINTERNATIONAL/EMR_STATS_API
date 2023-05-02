from django.db import models
from facilities.models import Facility 

# Create your models here.
class Enconters(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    program_name = models.CharField(max_length=100)
    total_encounters = models.BigIntegerField()
    total_patients = models.BigIntegerField()
    encounter_date = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'encounters'

    def __str__(self) -> str:
        return super().__str__()
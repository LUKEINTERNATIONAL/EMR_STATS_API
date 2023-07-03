from django.db import models
from facilities.models import Facility 

# Create your models here.
class ViralLoad(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    accession_number = models.CharField(max_length=100, unique=True)
    person_id = models.CharField(max_length=100)
    results = models.CharField(max_length=100,blank=True)
    order_status = models.CharField(max_length=100,blank=True)
    test_reason = models.CharField(max_length=100,blank=True)
    acknowledgement_type = models.CharField(max_length=100,blank=True)
    ordered_date = models.DateTimeField(null=True)
    released_date = models.DateTimeField(null=True)
    acknowledgement_date = models.CharField(max_length=100,blank=True,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'viral_load'

    def __str__(self) -> str:
        return super().__str__()
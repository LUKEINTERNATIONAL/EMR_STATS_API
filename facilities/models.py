from django.db import models

# Create your models here.
class Facility(models.Model):
    facility_name = models.CharField(max_length=100,blank=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    district_id = models.BigIntegerField()
    ip_address = models.CharField(max_length=100, unique=True,blank=True)
    latitude = models.CharField(max_length=100,blank=True)
    longitude = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'facilities'

    def __str__(self) -> str:
        return super().__str__()
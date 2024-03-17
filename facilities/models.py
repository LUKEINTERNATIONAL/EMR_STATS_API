from django.db import models

# Create your models here.
class Facility(models.Model):
    facility_name = models.CharField(max_length=100,blank=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100, unique=True,blank=True)
    user_name_iblis = models.CharField(max_length=100,blank=True)
    password_iblis = models.CharField(max_length=100,blank=True)
    ip_address_iblis = models.CharField(max_length=100,blank=True)
    district_id = models.BigIntegerField()
    latitude = models.CharField(max_length=100,blank=True)
    longitude = models.CharField(max_length=100,blank=True)
    viral_load = models.CharField(max_length=100,blank=True)
    dde_enabled = models.CharField(max_length=100,blank=True)
    close_monitoring_status = models.CharField(max_length=100,blank=True)
    get_device_status = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'facilities'

    def __str__(self) -> str:
        return super().__str__()
from django.db import models
from facilities.models import Facility 

# Create your models here.
class Device(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100,blank=True)
    device_ip = models.CharField(max_length=100,blank=True)
    device_status = models.CharField(max_length=100,blank=True)
    device_mac = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'device'

    def __str__(self) -> str:
        return super().__str__()
    
class DeviceServices(models.Model):
    device_ip = models.CharField(max_length=100)
    port = models.CharField(max_length=100,blank=True)
    state = models.CharField(max_length=100,blank=True)
    service = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'device_services'

    def __str__(self) -> str:
        return super().__str__()
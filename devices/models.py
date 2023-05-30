from django.db import models
from facilities.models import Facility 

# Create your models here.
class Device(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100,blank=True)
    device_ip_address = models.CharField(max_length=100,blank=True)
    device_status = models.CharField(max_length=100)
    device_mac = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'device'

    def __str__(self) -> str:
        return super().__str__()
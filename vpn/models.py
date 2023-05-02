from django.db import models
from facilities.models import Facility 

# Create your models here.
class VPN(models.Model):
    id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    start_down_time = models.CharField(max_length=100,blank=True)
    end_down_time = models.CharField(max_length=100,blank=True)
    response_time = models.CharField(max_length=100,blank=True)
    vpn_status = models.CharField(max_length=100)
    vpn_sms_status = models.CharField(max_length=100,blank=True)
    date = models.CharField(max_length=100)

    class Meta:
       managed = True
       db_table = 'vpn'

    def __str__(self) -> str:
        return super().__str__()
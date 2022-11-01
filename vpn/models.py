from django.db import models
from facilities.models import Facility 

# Create your models here.
class VPN(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    vpn_status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    class Meta:
       managed = True
       db_table = 'vpn'

    def __str__(self) -> str:
        return super().__str__()
from django.db import models
from facilities.models import Facility 

# Create your models here.
class VPNTemp(models.Model):
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    vpn_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'vpn_temp'

    def __str__(self) -> str:
        return super().__str__()
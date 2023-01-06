from django.db import models

# Create your models here.
class Facility(models.Model):
    facility_name = models.CharField(max_length=100,blank=True)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'facilities'

    def __str__(self) -> str:
        return super().__str__()
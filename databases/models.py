from django.db import models

# Create your models here.
class Databases(models.Model):
    facility_name = models.CharField(max_length=100)
    dump_name = models.CharField(max_length=100)
    progress = models.CharField(max_length=100)
    database_name = models.CharField(max_length=100,blank=True)
    database_username = models.CharField(max_length=100,blank=True)
    server_ip_address = models.CharField(max_length=100,blank=True)
    database_password = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'databases'

    def __str__(self) -> str:
        return super().__str__()
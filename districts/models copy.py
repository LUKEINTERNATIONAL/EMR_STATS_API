from django.db import models

# Create your models here.
class District(models.Model):
    district = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'district'

    def __str__(self) -> str:
        return super().__str__()
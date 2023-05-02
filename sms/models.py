from django.db import models

# Create your models here.
class SMS(models.Model):
    user_id = models.CharField(max_length=100,blank=True)
    sms_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'sms'

    def __str__(self) -> str:
        return super().__str__()
from django.db import models

# Create your models here.
class Email(models.Model):
    user_id = models.CharField(max_length=100,blank=True)
    email_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       managed = True
       db_table = 'emails'

    def __str__(self) -> str:
        return super().__str__()
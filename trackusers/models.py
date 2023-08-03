from django.db import models
from users.models import CustomUser 

# Create your models here.
class TrackUsers(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    login_time = models.CharField(max_length=100,blank=True)
    logout_time = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'track_users'

    def __str__(self) -> str:
        return super().__str__()
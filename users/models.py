from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, username, password,**kwargs):
        """
        Creates and saves a User with the given username, password
        """
        if not username:
            raise ValueError('Users must have an username address')
        
        user = self.model(
            username=username,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,name=''):
        user = self.create_user(username,name=name,password=password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
        )
    name = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=100,blank=True)
    district_id = models.BigIntegerField(default=1)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name if self.name else self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
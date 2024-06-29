from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
        
    def __str__(self):
        return self.username


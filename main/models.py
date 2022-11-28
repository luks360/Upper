from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

class User(AbstractBaseUser):
    
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=200)

    objects = UserManager()

    USERNAME_FIELD = 'username'
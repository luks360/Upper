import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_staff = models.BooleanField(null=True)
    is_superuser = models.BooleanField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"


class GroupSpending(models.Model):

    name = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.name


class GroupProfits(models.Model):

    name = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.name


class Spending(models.Model):

    name = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="")
    group = models.ForeignKey(GroupSpending, on_delete=models.CASCADE)
    date = models.DateField()


class Profits(models.Model):
    name = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default="")
    group = models.ForeignKey(GroupProfits, on_delete=models.CASCADE)
    date = models.DateField()

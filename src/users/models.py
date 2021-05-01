from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(blank=True, null=True)
    email = models.EmailField()
    verification_code = models.CharField(max_length=15, null=True)


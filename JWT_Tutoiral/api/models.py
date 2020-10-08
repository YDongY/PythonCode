from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    token = models.CharField(max_length=64, null=True, blank=True)

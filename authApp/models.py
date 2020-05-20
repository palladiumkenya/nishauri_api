from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import CustomUserManager


class User(AbstractUser):
    username = None
    is_staff = None
    is_superuser = None
    msisdn = models.CharField(max_length=15, unique=True)
    CCCNo = models.CharField(max_length=15, unique=True)
    securityQuestion = models.CharField(null=True, blank=True, max_length=150)
    securityAnswer = models.CharField(max_length=50)
    termsAccepted = models.BooleanField(default=0)
    REQUIRED_FIELDS = ['CCCNo', 'securityQuestion', 'securityAnswer', 'termsAccepted']
    USERNAME_FIELD = 'msisdn'

    objects = CustomUserManager()

    def __str__(self):
        return self.msisdn

    class Meta:
        db_table = "User"

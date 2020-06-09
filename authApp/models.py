from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .manager import CustomUserManager
import uuid


class User(AbstractUser):
    username = None
    is_staff = None
    is_superuser = None
    first_name = models.CharField(null=True, blank=True, max_length=250)
    msisdn = models.CharField(max_length=15, unique=True)
    CCCNo = models.CharField(max_length=15, unique=True)
    securityQuestion = models.CharField(null=True, blank=True, max_length=150)
    securityAnswer = models.CharField(max_length=250)
    termsAccepted = models.BooleanField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # jwt_secret = models.UUIDField(default=uuid.uuid4)

    REQUIRED_FIELDS = ['CCCNo', 'securityQuestion', 'securityAnswer', 'termsAccepted']
    USERNAME_FIELD = 'msisdn'

    objects = CustomUserManager()

    def __str__(self):
        return self.msisdn

    class Meta:
        db_table = "User"
#
# def jwt_get_secret_key(user_model):
#     return user_model.jwt_secret


class Dependants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heiNumber = models.CharField(max_length=20, blank=False, unique=True)
    dob = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=0)

    class Meta:
        db_table = "Dependants"

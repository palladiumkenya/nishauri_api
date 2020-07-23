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
    last_name = models.CharField(null=True, blank=True, max_length=250)
    msisdn = models.CharField(max_length=15, unique=True)
    CCCNo = models.CharField(max_length=15, unique=True)
    securityQuestion = models.CharField(null=True, blank=True, max_length=150)
    securityAnswer = models.CharField(max_length=250)
    termsAccepted = models.BooleanField(default=0)
    initial_facility = models.CharField(max_length=50, default=0)
    current_facility = models.CharField(max_length=50, default=0)
    language_preference = models.CharField(max_length=20, default='English')
    consent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    first_name = models.CharField(max_length=60, blank=False)
    surname = models.CharField(max_length=60, null=True, blank=True)
    heiNumber = models.CharField(max_length=20, blank=False)
    dob = models.DateField(blank=True, null=True)
    approved = models.BooleanField(default=0)

    class Meta:
        db_table = "Dependants"


class Facilities(models.Model):
    mfl_code = models.PositiveIntegerField()
    name = models.CharField(max_length=80)
    county = models.CharField(max_length=30)
    sub_county = models.CharField(max_length=80)

    class Meta:
        db_table = "Facilities"

from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = {'id', 'msisdn', 'password', 'CCCNo', 'securityQuestion', 'securityAnswer', 'termsAccepted'}

import re, requests

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'msisdn', 'password', 'CCCNo', 'securityQuestion', 'securityAnswer', 'termsAccepted']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_securityAnswer(self, value):
        if not value:
            raise serializers.ValidationError("Invalid security Answer")
        else:
            value = make_password(value)
            return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Provide a password")
        elif validate_password(value) is None:
            value = make_password(value)
            return value
        else:
            validate_password(value)

    def validate_CCCNo(self, value):
        user = {
            "mfl_code": "12345",
            "ccc_number": value
        }
        url = "http://ushaurinode.mhealthkenya.org/api/mlab/check/consent"
        headers = {
            'content-type': "application/json",
            'Accept': 'application/json'
        }
        response = requests.post(url, data=user, json=headers)
        boo = response.headers
        if boo['Content-Length'] != '0':
            return value
        else:
            raise serializers.ValidationError("CCC number not found")
        # return boo


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'msisdn', 'CCCNo',
                  'termsAccepted', 'groups', 'user_permissions', 'user']


class DependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependants
        fields = '__all__'
        user = serializers.Field(source='user.id')


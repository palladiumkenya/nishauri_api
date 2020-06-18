import requests

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers


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
            "mfl_code": value[:5],
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


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    # d = Dependants.objects.get(user=user)
    print(user)
    class Meta:
        model = User
        fields = ['id', 'last_login', 'first_name', 'last_name', 'msisdn', 'CCCNo', 'termsAccepted',
                 'is_active', 'date_joined', 'securityQuestion', 'securityAnswer', 'user']


class DependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependants
        fields = '__all__'
        user = serializers.Field(source='user.id')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['msisdn', 'first_name', 'last_name', 'securityQuestion', 'securityAnswer']

    def validate_securityAnswer(self, value):
        if not value:
            raise serializers.ValidationError("Invalid security Answer")
        else:
            value = make_password(value)
            return value


class DependantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependants
        fields = ['first_name', 'surname']

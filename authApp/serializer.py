from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = {'id', 'msisdn', 'password', 'CCCNo', 'securityQuestion', 'securityAnswer', 'termsAccepted'}


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


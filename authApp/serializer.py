import requests
import datetime
from datetime import date
from datetime import datetime
from dateutil import relativedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from appointments.models import Appointments
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
            "ccc_number": value
        }
        url = "http://ushaurinode.mhealthkenya.org/api/mlab/get/one/client"
        headers = {
            'content-type': "application/json",
            'Accept': 'application/json'
        }
        response = requests.post(url, data=user, json=headers)
        boo = response.json()
        if len(boo['clients']) > 0:
            return value
        else:
            raise serializers.ValidationError("CCC number not found")

    def validate_language_preference(self, value):
        if value == 'English' or value == 'Kiswahili':
            return value
        else:
            return 'English'


class UserCreateAdmin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Provide a password")
        elif validate_password(value) is None:
            value = make_password(value)
            return value
        else:
            validate_password(value)


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'first_name', 'last_name', 'language_preference', 'msisdn', 'CCCNo',
                  'current_facility', 'initial_facility', 'termsAccepted', 'is_active', 'date_joined',
                  'securityQuestion', 'securityAnswer', 'user', 'chat_number']


class DependantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dependants
        fields = '__all__'
        user = serializers.Field(source='user.id')

    def validate_heiNumber(self, value):
        if Dependants.objects.filter(heiNumber=value).count() < 2:
            return value
        else:
            raise serializers.ValidationError("Dependant already has 2 approved care-givers")

    def to_representation(self, value):
        data = super().to_representation(value)
        print("a",data)
        dob = data["dob"]
        date1 = datetime.strptime(str(dob), '%Y-%m-%d')
        date2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
        diff = relativedelta.relativedelta(date2, date1)
        months_difference = "0 years"
        if diff.years == 0:
            months_difference = '{} months {} days'.format(diff.months, diff.days)
            data.update({"age": months_difference})
        else:
            months_difference = '{} years {} months {} days'.format(diff.years, diff.months, diff.days)
            data.update({"age": months_difference})
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['msisdn', 'first_name', 'last_name', 'language_preference', 'securityQuestion', 'securityAnswer']

    def validate_securityAnswer(self, value):
        if not value:
            raise serializers.ValidationError("Invalid security Answer")
        else:
            return value


class DependantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependants
        fields = ['first_name', 'surname']


class RegimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiment
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = '__all__'


class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'CCCNo', 'current_facility', 'msisdn']

    def to_representation(self, value):
        data = super().to_representation(value)

        code = data["current_facility"]
        data.update({'current_facility': Facilities.objects.get(mfl_code=code).name})

        return data
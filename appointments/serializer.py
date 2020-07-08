from rest_framework import serializers
from .models import *


class AppointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = "__all__"


class PAppointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ("id", "appntmnt_date", "app_status", "visit_type", "app_type")

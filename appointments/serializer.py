from rest_framework import serializers
from .models import *


class AppointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = "__all__"


class BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAppointment
        fields = "__all__"

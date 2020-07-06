from rest_framework import serializers
from .models import *


class AppointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ('appntmnt_date', 'app_status', 'visit_type')

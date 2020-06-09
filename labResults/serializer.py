from rest_framework import serializers
from labResults.models import LabResult


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

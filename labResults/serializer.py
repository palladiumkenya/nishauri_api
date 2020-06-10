from rest_framework import serializers
from labResults.models import *


class VLSerializer(serializers.ModelSerializer):
    class Meta:
        model = VLResult
        fields = '__all__'


class EidSerializer(serializers.ModelSerializer):
    class Meta:
        model = EidResults
        fields = '__all__'

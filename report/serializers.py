from rest_framework import serializers
from .models import *

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class IsBlindRequestSerializer(serializers.Serializer):
    targetId = serializers.IntegerField(source='target_id')
    type = serializers.CharField()
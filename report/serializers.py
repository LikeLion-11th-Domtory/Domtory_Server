from rest_framework import serializers
from .models import *

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        
# class UpdateReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Report
#         fields = ['id', 'status']
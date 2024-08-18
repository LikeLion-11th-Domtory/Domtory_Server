from rest_framework import serializers
from report.models.report_models import *

# class ReportRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Report
#         fields = ['reported_at']

class ReportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'status', 'reported_at', 'post']

class ReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'status', 'reported_at', 'comment']

class ReportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'status', 'reported_at', 'message']
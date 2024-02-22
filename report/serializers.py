from rest_framework import serializers
from .models import *

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class IsBlindRequestSerializer(serializers.Serializer):
    postOrCommentId = serializers.IntegerField(source='post_or_comment_id')
    type = serializers.CharField()
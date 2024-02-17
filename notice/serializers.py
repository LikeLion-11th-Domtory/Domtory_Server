from rest_framework import serializers
from .models import NoticeList

# Create your serializers here.

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeList
        fields = ['id', 'post_id', 'title', 'date', 'content', 'images', 'notice_url']
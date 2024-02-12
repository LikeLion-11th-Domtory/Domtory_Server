from rest_framework import serializers
from ..models import *
from .comment_serializer import *
from django.utils import timezone
from datetime import timedelta

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class ImageRequestSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child = serializers.ImageField())
    class Meta:
        model = PostImage
        fields = ['images']


class PostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body']


class PostResponseSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    post_image = PostImageSerializer(many = True)
    comment = CommentResponseSerializer(many = True)
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'

    def get_comment(self, obj):
        comments = obj.comment.filter(parent__isnull=True)
        serializer = CommentResponseSerializer(comments, many=True).data
        return serializer
    
    def get_status(self, obj):
        return obj.member.status

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d %H:%M')


class PostSimpleSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'member', 'status', 'title', 'thumbnail_url', 'created_at']

    def get_status(self, obj):
        return obj.member.status
    
    def get_created_at(self, obj):
        time_difference = timezone.now() - obj.created_at
        minutes = time_difference.total_seconds() / 60

        if time_difference <= timedelta(hours=1):
            # 1시간 이내인 경우
            return f'{int(minutes)}분 전'
        elif obj.created_at.date() == timezone.now().date():
            # 같은 날(오늘)인 경우
            return obj.created_at.strftime('%H시 %M분')
        else:
            # 이전 날짜인 경우
            return obj.created_at.strftime('%m/%d')
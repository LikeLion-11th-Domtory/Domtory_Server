from rest_framework import serializers
from ..models import *
from .comment_serializer import *

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
    post_image = PostImageSerializer(many = True)
    comment = CommentResponseSerializer(many = True)
    class Meta:
        model = Post
        fields = '__all__'

    def get_comment(self, obj):
        comments = obj.comment.filter(parent__isnull=True)
        serializer = CommentResponseSerializer(comments, many=True).data
        return serializer


class PostSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'member', 'title', 'thumbnail_url', 'created_at']
from rest_framework import serializers
from ..models import *
from .comment_serializer import *

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'board', 'title', 'body']


class PostResponseSerializer(serializers.ModelSerializer):
    post_image = PostImageSerializer(many = True)
    comment = CommentResponseSerializer(many = True)
    class Meta:
        model = Post
        fields = '__all__'
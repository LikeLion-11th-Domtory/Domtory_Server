from rest_framework import serializers
from ..models import Comment

class ReplyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'body']


class ReplyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'member', 'parent', 'body', 'created_at', 'is_blocked', 'is_deleted']


class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'body']


class CommentResponseSerializer(serializers.ModelSerializer):
    reply = ReplyResponseSerializer(many = True)
    class Meta:
        model = Comment
        fields = ['id', 'member', 'body', 'created_at', 'is_blocked', 'is_deleted', 'reply']
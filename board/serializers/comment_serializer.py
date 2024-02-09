from rest_framework import serializers
from ..models import Comment

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        models = Comment
        fields = ['id', 'parent', 'member', 'body', 'created_at', 'is_blocked', 'is_deleted']


class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        models = Comment
        fields = ['id', 'member', 'post', 'body']


class CommentResponseSerializer(serializers.ModelSerializer):
    reply = CommentRequestSerializer(many = True)
    class Meta:
        models = Comment
        fields = ['id', 'member', 'body', 'created_at', 'is_blocked', 'is_deleted', 'reply']
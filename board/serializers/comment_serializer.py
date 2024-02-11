from rest_framework import serializers
from ..models import Comment

class ReplyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent_id', 'body']


class ReplyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'member_id', 'parent_id', 'body', 'created_at', 'is_blocked', 'is_deleted']


class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'member_id', 'post_id', 'body']


class CommentResponseSerializer(serializers.ModelSerializer):
    reply = CommentRequestSerializer(many = True)
    class Meta:
        model = Comment
        fields = ['id', 'member_id', 'body', 'created_at', 'is_blocked', 'is_deleted', 'reply']
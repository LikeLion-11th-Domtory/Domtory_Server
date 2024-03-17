from rest_framework import serializers
from ..models import Comment
from django.utils import timezone

class ReplyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'body']


class ReplyResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'member', 'parent', 'body', 'anonymous_number', 'created_at', 'is_blocked', 'is_deleted', 'likes_cnt']

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%m/%d %H:%M')


class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'body']


class CommentResponseSerializer(serializers.ModelSerializer):
    reply = ReplyResponseSerializer(many = True)
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'member', 'body', 'created_at', 'anonymous_number', 'is_blocked', 'is_deleted', 'reply', 'likes_cnt']

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%m/%d %H:%M')
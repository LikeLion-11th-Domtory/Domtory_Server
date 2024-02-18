from rest_framework import serializers
from ..models import Comment

class ReplyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'body']


class ReplyResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'member', 'parent', 'body', 'created_at', 'is_blocked', 'is_deleted']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d %H:%M')


class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'body']


class CommentResponseSerializer(serializers.ModelSerializer):
    reply = ReplyResponseSerializer(many = True)
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'member', 'body', 'created_at', 'is_blocked', 'is_deleted', 'reply']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d %H:%M')
    

class CommentMyPageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'member', 'post', 'body', 'created_at', 'is_blocked']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%m/%d %H:%M')
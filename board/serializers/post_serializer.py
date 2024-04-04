from rest_framework import serializers
from ..models import *
from .comment_serializer import *
from django.utils import timezone
from datetime import timedelta
from board.models import PostMemberBookmark, PostMemberLike

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
    comment = CommentResponseSerializer(many = True, read_only = True)
    created_at = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
    
    def get_status(self, obj):
        return obj.member.status

    def get_created_at(self, obj):
        post_time = timezone.localtime(obj.created_at)
        if obj.board.pk != 6:
            time_difference = timezone.now() - obj.created_at
            minutes = time_difference.total_seconds() / 60

            if time_difference <= timedelta(hours=1):
                # 1시간 이내인 경우
                return f'{int(minutes)}분 전'
            elif post_time.date() == timezone.localtime(timezone.now()).date():
                # 같은 날(오늘)인 경우
                return post_time.strftime('%H:%M')
            else:
                # 이전 날짜인 경우
                print(obj.created_at)
                print(timezone.now())
                return post_time.strftime('%m/%d')
        else:
            return post_time.strftime('%Y-%m-%d')
    
    def get_owner(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.member: return True
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if PostMemberBookmark.objects.filter(post = obj, member = request.user.id):
            return True
        return False
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if PostMemberLike.objects.filter(post = obj, member = request.user.id):
            return True
        return False
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.board.pk == 6:
            representation['date'] = representation.pop('created_at')
        return representation


class PostSimpleSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'member', 'board', 'status', 'title', 'body', 'comment_cnt', 'thumbnail_url', 'created_at', 'likes_cnt', 'bookmark_cnt']

    def get_status(self, obj):
        return obj.member.status
    
    def get_created_at(self, obj):
        post_time = timezone.localtime(obj.created_at)
        if obj.board.pk != 6:
            time_difference = timezone.now() - obj.created_at
            minutes = time_difference.total_seconds() / 60

            if time_difference <= timedelta(hours=1):
                # 1시간 이내인 경우
                return f'{int(minutes)}분 전'
            elif post_time.date() == timezone.localtime(timezone.now()).date():
                # 같은 날(오늘)인 경우
                return post_time.strftime('%H:%M')
            else:
                # 이전 날짜인 경우
                print(obj.created_at)
                print(timezone.now())
                return post_time.strftime('%m/%d')
        else:
            return post_time.strftime('%Y-%m-%d')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.board.pk == 6:
            representation['date'] = representation.pop('created_at')
        return representation
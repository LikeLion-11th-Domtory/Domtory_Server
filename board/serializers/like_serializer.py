from rest_framework import serializers
from board.models.like_models import *

class PostLikeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMemberLike
        fields = '__all__'


class CommentLikeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentMemberLike
        fields = '__all__'
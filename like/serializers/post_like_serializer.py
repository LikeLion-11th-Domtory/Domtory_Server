from rest_framework import serializers
from like.models.post_member_like_models import PostMemberLike

class PostLikeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMemberLike
        fields = '__all__'
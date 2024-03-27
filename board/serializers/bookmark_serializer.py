from rest_framework import serializers
from board.models.bookmark_models import PostMemberBookmark

class PostBookmarkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMemberBookmark
        fields = '__all__'
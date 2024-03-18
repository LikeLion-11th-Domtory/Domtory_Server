from rest_framework import serializers
from push.domains import NotificationDetail

class TokenRequestSerializer(serializers.Serializer):
    pushToken = serializers.CharField(source='push_token')

class PushListResponseSerializer(serializers.Serializer):
    memberId = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()
    pushedAt = serializers.CharField()
    transformedPushedAt = serializers.CharField()
    boardId = serializers.IntegerField(allow_null=True)
    postId = serializers.IntegerField(allow_null=True)
    isChecked = serializers.BooleanField()

class PushCheckRequestSerialzier(serializers.Serializer):
    memberId = serializers.IntegerField(source='member_id')
    pushedAt = serializers.CharField(source='pushed_at')
    
class NotificationDetailResponseSerializer(serializers.ModelSerializer):
    lightningPost = serializers.BooleanField(source='lightning_post')

    class Meta:
        model = NotificationDetail
        fields = ('breakfast', 'lunch', 'dinner', 'lightningPost', 'comment', 'reply',)
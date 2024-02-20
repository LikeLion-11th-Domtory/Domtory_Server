from rest_framework import serializers

class TokenRequestSerializer(serializers.Serializer):
    pushToken = serializers.CharField(source='push_token')

class PushListResponseSerializer(serializers.Serializer):
    memberId = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()
    pushedAt = serializers.CharField()
    boardId = serializers.IntegerField(allow_null=True)
    postId = serializers.IntegerField(allow_null=True)
    isChecked = serializers.BooleanField()
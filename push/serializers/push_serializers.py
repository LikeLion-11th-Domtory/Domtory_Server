from rest_framework import serializers

class TokenSendRequestSerializer(serializers.Serializer):
    pushToken = serializers.CharField(source='push_token')
from rest_framework import serializers

class TokenRequestSerializer(serializers.Serializer):
    pushToken = serializers.CharField(source='push_token')
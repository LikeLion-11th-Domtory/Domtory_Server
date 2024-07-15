from rest_framework import serializers


class IsBlindRequestSerializer(serializers.Serializer):
    targetId = serializers.IntegerField(source='target_id')
    type = serializers.CharField()
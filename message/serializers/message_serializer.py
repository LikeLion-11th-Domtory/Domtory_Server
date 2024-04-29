from django.utils import timezone
from rest_framework import serializers

from ..domains.message_block_models import MessageBlock
from ..domains.message_models import Message


class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['body']

class MessageResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'send_id', 'recv_id', 'body', 'created_at']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

class MessageSimpleSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_received = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'send_id', 'recv_id', 'body', 'created_at', 'is_read', 'is_received']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

    def get_is_received(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.recv_id:
                return True
        return False

class MessageBlockResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBlock
        fields = '__all__'

class MessageBlockRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageBlock
        fields = []
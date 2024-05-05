from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from member.domains import Member
from ..domains.message_block_models import MessageBlock
from ..domains.message_models import Message


class MessageRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['body']

class MessageResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_received = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'body', 'created_at', 'is_read', 'is_received']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

    def get_is_received(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.receiver:
                return True
        return False

class MessageSimpleSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_received = serializers.SerializerMethodField()
    new_messages_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'body', 'created_at', 'is_read', 'is_received', 'new_messages_cnt']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

    def get_is_received(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.receiver:
                return True
        return False

    def get_new_messages_cnt(self, obj):
        request = self.context.get('request')
        if request.user == obj.sender:
            return 0
        else:
            new_messages = Message.objects.filter(Q(sender__id = obj.sender.id) & Q(receiver__id = obj.receiver.id) & Q(is_read = False))
            return len(new_messages)

class MessageBlockResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBlock
        fields = '__all__'

class MessageBlockRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageBlock
        fields = []
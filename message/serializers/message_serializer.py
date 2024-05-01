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

class MessageSimpleSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    is_received = serializers.SerializerMethodField()
    new_messages_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'send_id', 'recv_id', 'body', 'created_at', 'is_read', 'is_received', 'new_messages_cnt']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

    def get_is_received(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.recv_id:
                return True
        return False

    def get_new_messages_cnt(self, obj):
        request = self.context.get('request')
        if request.user == obj.send_id:
            return 0
        else:
            sender = Member.objects.get(pk=obj.send_id.id)
            receiver = Member.objects.get(pk=obj.recv_id.id)
            new_messages = Message.objects.filter(Q(send_id = sender) & Q(recv_id = receiver) & Q(is_read = False))
            return len(new_messages)

class MessageBlockResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBlock
        fields = '__all__'

class MessageBlockRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageBlock
        fields = []
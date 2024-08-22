from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ..domains import Message, MessageRoom, MessageBlock


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
    message_room_id = serializers.SerializerMethodField()
    counterpart = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'counterpart', 'body', 'created_at', 'is_read', 'is_received', 'new_messages_cnt', 'message_room_id']

    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%y/%m/%d %H:%M')

    def get_is_received(self, obj):
        request = self.context.get('request')
        if request:
            if request.user == obj.receiver:
                return True
        return False
    
    def get_counterpart(self, obj):
        if self.get_is_received(obj):
            return obj.sender_id
        else:
            return obj.receiver_id

    def get_new_messages_cnt(self, obj):
        request = self.context.get('request')
        if request.user == obj.sender:
            return 0
        else:
            new_messages = Message.objects.filter(Q(sender = obj.sender) & Q(receiver = obj.receiver) & Q(is_read = False))
            return len(new_messages)

    def get_message_room_id(self, obj):
        return obj.message_room_id


class MessageRoomRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageRoom
        fields = []

class MessageRoomResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageRoom
        fields = ['id', 'board', 'post_title', 'receiver_anonymous_num']


class MessageBlockResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageBlock
        fields = '__all__'

class MessageBlockRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageBlock
        fields = []
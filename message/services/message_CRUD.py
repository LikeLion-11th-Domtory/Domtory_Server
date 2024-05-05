from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from member.domains import Member
from utils.exceptions.message_exception import MessageBlockedError, MessageToMeError
from ..domains.message_block_models import MessageBlock
from ..domains.message_models import Message
from ..serializers.message_serializer import MessageRequestSerializer, MessageResponseSerializer, \
    MessageSimpleSerializer


def get_message_detail(request, message_id):
    message = get_object_or_404(Message, id = message_id)
    response = MessageResponseSerializer(message, context={'request' : request}).data
    return response

def create_message(request, target_id):
    serializer = MessageRequestSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    receiver = Member.objects.get(pk=target_id)

    try:
        block = MessageBlock.objects.get(requester=request.user, target=receiver)
    except MessageBlock.DoesNotExist:
        block = None
    try:
        blocked = MessageBlock.objects.get(requester=receiver, target=request.user)
    except MessageBlock.DoesNotExist:
        blocked = None
    if block or blocked:
        raise MessageBlockedError
    if request.user == receiver:
        raise MessageToMeError

    message = serializer.save(sender=request.user, receiver=receiver)
    return get_message_detail(request, message.id)

@transaction.atomic
def update_message(request, target_id):
    receiver = request.user
    sender = Member.objects.get(pk=target_id)
    # 현재 접속한 유저가 받은 & target 유저가 보낸 & 아직 읽지 않은 메시지
    unread_messages = Message.objects.filter(is_read = False, sender = sender, receiver = receiver).order_by('created_at')
    for message in unread_messages:
        message.is_read = True
        message.save(update_fields=['is_read'])
    response = {
        "msg": "쪽지 읽음 처리 완료"
    }
    return response

@transaction.atomic
def delete_messages(request, target_id):
    sender = request.user
    receiver = Member.objects.get(pk=target_id)
    sent_messages = Message.objects.filter(sender=sender, receiver=receiver)
    received_messages = Message.objects.filter(sender=receiver, receiver=sender)

    for sent_message in sent_messages:
        sent_message.is_deleted_send = True
        sent_message.save(update_fields=['is_deleted_send'])
    for received_message in received_messages:
        received_message.is_deleted_recv = True
        received_message.save(update_fields=['is_deleted_recv'])
    response = {
        "msg": "쪽지 삭제 완료"
    }
    return response

def get_message_list(request):
    user_id = request.user.id
    messages = Message.objects.filter(Q(receiver = user_id) | Q(sender = user_id)) # 현재 유저가 주고받은 메시지
    partners = [] # 현재 유저와 쪽지 주고받은 대상의 pk를 저장
    for message in messages:
        if message.receiver.id in partners or message.sender.id in partners:
            continue
        if message.receiver.id == user_id:
            partners.append(message.sender.id)
        if message.sender.id == user_id:
            partners.append(message.receiver.id)

    recent_messages = [] # 현재 유저가 쪽지 주고받은 대상과 나눈 가장 최근 쪽지 저장
    for partner_id in partners:
        recent_message = Message.objects.filter((Q(sender__id = partner_id) & Q(receiver__id = user_id)) | (Q(sender__id = user_id) & Q(receiver__id = partner_id))).order_by('-created_at')[0]
        if recent_message.sender.id == user_id:
            if recent_message.is_deleted_send:
                continue
        elif recent_message.receiver.id == user_id:
            if recent_message.is_deleted_recv:
                continue
        recent_messages.append(recent_message)

    response = MessageSimpleSerializer(recent_messages, many=True, context={'request' : request}).data
    return response

def get_specific_message_list(request, target_id):
    sender = request.user
    receiver = Member.objects.get(pk=target_id)
    messages = Message.objects.filter((Q(sender = sender) & Q(receiver = receiver)) | (Q(sender = receiver) & Q(receiver = sender))).order_by('created_at')
    response = MessageResponseSerializer(messages, many=True, context={'request' : request}).data
    return response

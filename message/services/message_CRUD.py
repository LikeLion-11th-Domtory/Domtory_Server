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
        block = MessageBlock.objects.get(req_id=request.user, tar_id=receiver)
    except MessageBlock.DoesNotExist:
        block = None
    try:
        blocked = MessageBlock.objects.get(req_id=receiver, tar_id=request.user)
    except MessageBlock.DoesNotExist:
        blocked = None
    if block or blocked:
        raise MessageBlockedError
    if request.user == receiver:
        raise MessageToMeError

    message = serializer.save(send_id=request.user, recv_id=receiver)
    return get_message_detail(request, message.id)

def update_message(request, target_id):
    sender = request.user
    receiver = Member.objects.get(pk=target_id)
    unread_messages = Message.objects.filter(is_read = False, send_id = receiver, recv_id = sender).order_by('created_at')
    for message in unread_messages:
        message.is_read = True
        message.save(update_fields=['is_read'])
    response = {
        "msg": "쪽지 읽음 처리 완료"
    }
    return response

def delete_messages(request, target_id):
    sender = request.user
    receiver = Member.objects.get(pk=target_id)
    sent_messages = Message.objects.filter(send_id=sender, recv_id=receiver)
    received_messages = Message.objects.filter(send_id=receiver, recv_id=sender)

    for smsg in sent_messages:
        smsg.is_deleted_send = True
        smsg.save(update_fields=['is_deleted_send'])
    for rmsg in received_messages:
        rmsg.is_deleted_recv = True
        rmsg.save(update_fields=['is_deleted_recv'])
    response = {
        "msg": "쪽지 삭제 완료"
    }
    return response

def get_message_list(request):
    messages = Message.objects.filter(Q(recv_id = request.user) | Q(send_id = request.user))
    cands = []
    for m in messages:
        sender = Member.objects.get(pk=m.send_id.id)
        receiver = Member.objects.get(pk=m.recv_id.id)
        if (sender, receiver) in cands or (receiver, sender) in cands:
            continue
        cands.append((sender, receiver))
    print(cands)
    m_list = []
    for s, r in cands:
        cand = Message.objects.filter((Q(send_id = s) & Q(recv_id = r)) | (Q(send_id = r) & Q(recv_id = s))).order_by('-created_at')[0]
        if cand.send_id == request.user:
            if cand.is_deleted_send:
                continue
        elif cand.recv_id == request.user:
            if cand.is_deleted_recv:
                continue
        m_list.append(cand)

    response = MessageSimpleSerializer(m_list, many=True, context={'request' : request}).data
    return response

def get_specific_message_list(request, target_id):
    sender = request.user
    receiver = Member.objects.get(pk=target_id)
    messages = Message.objects.filter((Q(send_id = sender) & Q(recv_id = receiver)) | (Q(send_id = receiver) & Q(recv_id = sender))).order_by('created_at')
    response = MessageResponseSerializer(messages, many=True, context={'request' : request}).data
    return response

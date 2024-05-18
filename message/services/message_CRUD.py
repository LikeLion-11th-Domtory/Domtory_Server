from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from board.models import Post, Comment
from member.domains import Member
from utils.exceptions.message_exception import MessageBlockedError, MessageToMeError
from ..domains.message_block_models import MessageBlock
from ..domains.message_models import Message, MessageRoom
from ..serializers.message_serializer import MessageRequestSerializer, MessageResponseSerializer, \
    MessageSimpleSerializer, MessageRoomResponseSerializer, MessageRoomRequestSerializer


def get_message_detail(request, message_id):
    message = get_object_or_404(Message, id = message_id)
    response = MessageResponseSerializer(message, context={'request' : request}).data
    return response


def get_message_room(request, message_room_id):
    message_room = get_object_or_404(MessageRoom, id = message_room_id)
    response = MessageRoomResponseSerializer(message_room, context={'request' : request}).data
    return response


@transaction.atomic
def create_message_room(request, post_id, comment_anonymous_number):
    is_from_comment = True
    post = Post.objects.get(pk=post_id)
    sender = request.user
    sender_id = sender.id
    # comment_anonymous_number가 0이면 게시글 작성자가, 1 이상이면 댓글 작성자가 최초 수신자
    if comment_anonymous_number > 0:
        comment = Comment.objects.get(post=post, anonymous_number=comment_anonymous_number)
        target_id = comment.member_id
    else:
        is_from_comment = False
        target_id = post.member_id
    try:
        message_room = MessageRoom.objects.get(Q(post_id=post_id) &
                                               ((Q(first_sender_id=sender_id) & Q(first_receiver_id=target_id)) |
                                                (Q(first_sender_id=target_id) & Q(first_receiver_id=sender_id))))
    except MessageRoom.DoesNotExist:
        message_room = None

    # 이미 쪽지 기록이 존재할 때 => 리다이렉트용으로 message_room_id 리턴
    if message_room:
        response = {
            "message_room_id" : message_room.id
        }
        return response
    # 쪽지 기록이 존재하지 않을 때 => 새로운 쪽지방 만들고 정보 리턴
    else:
        serializer = MessageRoomRequestSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            post = Post.objects.get(pk=post_id)
            receiver_anonymous_num = -1
            if is_from_comment:
                receiver_anonymous_num = comment.anonymous_number
            message_info = serializer.save(post=post,
                                             receiver_anonymous_num=receiver_anonymous_num,
                                             first_sender_id=sender_id, first_receiver_id=target_id)
            return get_message_room(request, message_info.id)


@transaction.atomic
def create_message(request, message_room_id):
    serializer = MessageRequestSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)

    message_room = get_object_or_404(MessageRoom, id = message_room_id)
    sender = request.user
    if message_room.first_sender == sender:
        receiver = message_room.first_receiver
    else:
        receiver = message_room.first_sender

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

    message = serializer.save(sender=request.user, receiver=receiver, message_room=message_room)
    return get_message_detail(request, message.id)


@transaction.atomic
def read_message(request, message_room_id):
    receiver = request.user
    # 현재 접속한 유저가 받은 & target 유저가 보낸 & 아직 읽지 않은 메시지
    unread_messages = Message.objects.filter(is_read = False, message_room_id=message_room_id, receiver=receiver).order_by('created_at')
    for message in unread_messages:
        message.is_read = True
        message.save(update_fields=['is_read'])
    response = {
        "msg": "쪽지 읽음 처리 완료"
    }
    return response


@transaction.atomic
def delete_messages(request, message_room_id):
    sender = request.user
    sent_messages = Message.objects.filter(sender=sender, message_room_id=message_room_id)
    received_messages = Message.objects.filter(receiver=sender, message_room_id=message_room_id)

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
    message_rooms = MessageRoom.objects.filter(Q(first_receiver_id = user_id) | Q(first_sender_id = user_id)) # 현재 유저가 소속된 쪽지방
    recent_messages = []  # 현재 유저가 쪽지 주고받은 대상과 나눈 가장 최근 쪽지 저장
    for message_room in message_rooms:
        messages = Message.objects.filter(message_room=message_room).order_by('-created_at')
        if messages:
            recent_message = messages[0]
            if recent_message:
                if recent_message.sender_id == user_id:
                    if recent_message.is_deleted_send:
                        continue
                elif recent_message.receiver_id == user_id:
                    if recent_message.is_deleted_recv:
                        continue
                recent_messages.append(recent_message)

    response = MessageSimpleSerializer(recent_messages, many=True, context={'request' : request}).data
    return response


def get_specific_message_list(request, message_room_id):
    user = request.user
    messages = Message.objects.filter(message_room_id=message_room_id).order_by('created_at')
    not_deleted_messages = []
    for message in messages:
        if message.sender == user:
            if not message.is_deleted_send:
                not_deleted_messages.append(message)
        if message.receiver == user:
            if not message.is_deleted_recv:
                not_deleted_messages.append(message)
    response = MessageResponseSerializer(not_deleted_messages, many=True, context={'request' : request}).data
    return response

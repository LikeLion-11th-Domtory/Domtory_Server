from django.db.models import Q
from django.shortcuts import get_object_or_404

from member.domains import Member
from message.domains.message_block_models import MessageBlock
from message.serializers.message_serializer import MessageBlockRequestSerializer, MessageBlockResponseSerializer
from utils.exceptions.message_exception import AlreadyBlockedError


def get_message_block(request, message_block_id):
    block = get_object_or_404(MessageBlock, id=message_block_id)
    response = MessageBlockResponseSerializer(block, context={'request' : request}).data
    return response

def create_message_block(request, target_id):
    target = Member.objects.get(id = target_id)
    try:
        block = MessageBlock.objects.get(req_id=request.user, tar_id=target)
    except MessageBlock.DoesNotExist:
        block = None
    try:
        blocked = MessageBlock.objects.get(req_id=target, tar_id=request.user)
    except MessageBlock.DoesNotExist:
        blocked = None
    if not block and not blocked:
        serializer = MessageBlockRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        block = serializer.save(req_id=request.user, tar_id=target)
        return get_message_block(request, block.id)
    else:
        raise AlreadyBlockedError
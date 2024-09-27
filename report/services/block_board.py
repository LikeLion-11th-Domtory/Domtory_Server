from report.serializers.block_serializer import *
from django.shortcuts import get_object_or_404
from board.models.comment_models import *
from board.models.post_models import *


def block_board(request):
        is_blind_request_serializer = IsBlindRequestSerializer(data=request.data)
        is_blind_request_serializer.is_valid(raise_exception=True)
        is_blind_data = is_blind_request_serializer.validated_data

        post_or_comment_id = is_blind_data.get('target_id')
        type = is_blind_data.get('type')

        if type == "comment":
            target_comment = get_object_or_404(Comment, id=post_or_comment_id)
            target_comment.is_blocked = True
            target_comment.save(update_fields=['is_blocked'])

        elif type == "post":
            target_post = get_object_or_404(Post, id=post_or_comment_id)
            target_post.is_blocked = True
            target_post.save(update_fields=['is_blocked'])
        else:
            return TypeError
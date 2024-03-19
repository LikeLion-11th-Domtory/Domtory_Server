from board.models.like_models import CommentMemberLike
from board.serializers.like_serializer import CommentLikeRequestSerializer
from board.models.comment_models import *

from django.db.models import Q

from utils.exceptions.like_exception import (
        CommentAuthorExceptionError,
        CommentDuplicateLikeError,
    )


def create_comment_like(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)

     # request로 전달받은 CommentMemberLike 객체 직렬화, 검증, 저장
    comment_like_request_serializer = CommentLikeRequestSerializer(data={'comment':comment.id, 'member':request.user})
    comment_like_request_serializer.is_valid(raise_exception=True)
    comment_like_data = comment_like_request_serializer.save()

    comment_id = comment_like_data.comment
    member_id = comment_like_data.member

    #본인 댓글에 좋아요 금지
    if member_id == comment.member: #작성자는 좋아요를 누를 수 없음
        raise CommentAuthorExceptionError
    
    #좋아요 중복 금지
    q = Q(id=comment_id) & Q(member=member_id)
    if Comment.objects.filter(q).exists(): #쿼리 얼마나 쏘는지 체크
        raise CommentDuplicateLikeError


    comment.likes_cnt += 1
    comment.save(update_fields=['likes_cnt'])

    res = {
        "likes_cnt" : comment.likes_cnt
    }
    return res
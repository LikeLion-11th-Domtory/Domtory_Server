from board.models.like_models import CommentMemberLike
from board.serializers.like_serializer import CommentLikeRequestSerializer
from board.models.comment_models import *

from django.db.models import Q

from utils.exceptions.like_exception import (
        CommentAuthorExceptionError,
        CommentDuplicateLikeError,
    )


def create_comment_like(request, comment_id):
     # request로 전달받은 PostMemberLike 객체 직렬화, 검증, 저장
    comment_like_request_serializer = CommentLikeRequestSerializer(data=request.data, context={'comment':comment_id, 'member':request.user})
    comment_like_request_serializer.is_valid(raise_exception=True)
    comment_like_data = comment_like_request_serializer.validated_data

    comment_id = comment_like_data.get('comment')
    member_id = comment_like_data.get('member')
    get_liked_comment = Comment.objects.get(pk=comment_id) #좋아요 받은 Post객체 불러옴

    #본인 댓글에 좋아요 금지
    if member_id == get_liked_comment.member: #작성자는 좋아요를 누를 수 없음
        raise CommentAuthorExceptionError
    
    #좋아요 중복 금지
    q = Q(id=comment_id) & Q(member=member_id)
    if Comment.objects.filter(q).exists(): #쿼리 얼마나 쏘는지 체크
        raise CommentDuplicateLikeError


    get_liked_comment.likes_cnt += 1
    get_liked_comment.save(update_fields=['likes_cnt'])

    res = {
        "likes_cnt" : get_liked_comment.likes_cnt
    }
    return res
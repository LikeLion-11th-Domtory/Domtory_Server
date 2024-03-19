from board.models.like_models import *
from board.serializers.like_serializer import *
from board.models.popular_post_models import *
from board.models.post_models import *

from django.utils import timezone
from django.db.models import Q

from utils.exceptions.like_exception import (
        PostAuthorExceptionError,
        PostDuplicateLikeError,
    )

def create_post_like(request, post_id):
    post = Post.objects.get(pk=post_id)

    # request로 전달받은 PostMemberLike 객체 직렬화, 검증, 저장
    post_like_request_serializer = PostLikeRequestSerializer(data={'post':post.id, 'member':request.user.id})
    post_like_request_serializer.is_valid(raise_exception=True)
    post_like_data = post_like_request_serializer.save()


    post_id = post_like_data.post
    member_id = post_like_data.member

    #본인 게시글에 좋아요 금지
    if member_id == post.member: #작성자는 좋아요를 누를 수 없음
        raise PostAuthorExceptionError
    
    #좋아요 중복 금지
    q = Q(id=post_id) & Q(member=member_id)
    if Post.objects.filter(q).exists(): #쿼리 얼마나 쏘는지 체크
        raise PostDuplicateLikeError

    post.likes_cnt += 1
    post.save(update_fields=['likes_cnt'])

    #핫게 PopularPost 등록
    if post.likes_cnt == 5:
        # hot_post_response_serializer = PostResponseSerializer(get_liked_post)

        popular_at = timezone.now()
        new_popular_post = PopularPost(post=post_id, popular_at=popular_at)
        new_popular_post.save()

        """
        user에게 푸시 보내는 메서드 필요
        """

    res = {
        "likes_cnt" : post.likes_cnt
    }
    return res
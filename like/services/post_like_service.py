from like.models.post_member_like_models import *
from like.serializers.post_like_serializer import *

from django.utils import timezone

def create_post_like(request_post_like_data):

    # request로 전달받은 PostMemberLike 객체 직렬화, 검증
    post_like_request_serializer = PostLikeRequestSerializer(data=request_post_like_data)
    post_like_request_serializer.is_valid(raise_exception=True)
    post_like_data = post_like_request_serializer.validated_data

    # 좋아요 객체 != post 객체
    post_id = post_like_data.get('post')
    member_id = post_like_data.get('member')
    get_liked_post = Post.objects.get(pk=post_id) #좋아요 받은 Post객체 불러옴

    if member_id == get_liked_post.member: #try-except문? 
        return "내가 쓴 글은 공감할 수 없습니다."
    
    
    #클라이언트와의 교류 없음 -> serializer의 개입 필요없음!
    get_liked_post.likes_cnt += 1
    get_liked_post.save(update_fields=['liked_cnt'])

    #핫게 등록
    if get_liked_post.likes_cnt == 5:
        # hot_post_response_serializer = PostResponseSerializer(get_liked_post)

        hotpost_at = timezone.localtime()
        get_liked_post.hotpost_at = hotpost_at #실제로 필드 생성 필요함.
        get_liked_post.save(update_fields='hotpost_at')

        user = get_liked_post.member
        """
        user에게 푸시 보내는 메서드 필요
        """
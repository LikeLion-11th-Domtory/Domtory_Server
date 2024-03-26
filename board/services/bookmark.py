from board.models import PostMemberBookmark, Post
from board.serializers import PostBookmarkRequestSerializer

"""
스크랩 등록/취소 메소드
"""
def bookmark_post(request, post_id):
    post = Post.objects.get(pk = post_id)

    bookmark = PostMemberBookmark.objects.filter(post = post, member = request.user.id)
    if not bookmark:
        serializer = PostBookmarkRequestSerializer(data={'post':post.id, 'member':request.user.id})
        serializer.is_valid(raise_exception = True)
        serializer.save()

        post.bookmark_cnt += 1
        post.save(update_fields=['bookmark_cnt'])
        is_created = True
    else:
        instance = bookmark.first()
        instance.delete()
        
        post.bookmark_cnt -= 1
        post.save(update_fields=['bookmark_cnt'])
        is_created = False
    
    res = {
        "is_created" : is_created,
        "bookmark_cnt" : post.bookmark_cnt
    }
    return res
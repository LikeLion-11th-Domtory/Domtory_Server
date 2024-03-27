from board.models import PostMemberBookmark, Post
from board.serializers import PostBookmarkRequestSerializer, PostSimpleSerializer
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from operator import attrgetter
from django.db.models import Q

class PostPageNumberPagination(PageNumberPagination):
    """
    페이지네이션 클래스
    """
    page_size = 30

    def get_pages(self, data):
        return OrderedDict([
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            ('postList', data),
        ])


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


"""
스크랩한 게시글 리스트 메소드
"""
def bookmark_post_list(request):
    bookmarks = PostMemberBookmark.objects.filter(
    Q(member=request.user) & # 유저가 스크랩한 게시글
    Q(post__is_deleted=False) & # 게시글이 삭제되지 않은 경우
    Q(post__is_blocked=False)   # 게시글이 차단되지 않은 경우
    ).select_related('post')

    posts_queryset = [bookmark.post for bookmark in bookmarks]
    sorted_posts = sorted(posts_queryset, key=attrgetter('created_at'), reverse=True)
    
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(sorted_posts, request)
    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)
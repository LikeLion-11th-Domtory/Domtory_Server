
from board.models.popular_post_models import PopularPost
from board.models.board_models import Board
# from board.services.post_list import PostPageNumberPagination
from board.serializers.post_serializer import PostSimpleSerializer

from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
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
    

def get_popular_board_list(request):
    # PopularPost 객체들의 post까지 불러옴 
    get_popular_posts = PopularPost.objects.select_related('post').filter(post__is_blocked=False, post__is_deleted=False).order_by('-popular_at')
    popular_posts_data = get_popular_posts.post


    # 아래서부터는 정섭오빠 코드 참고함 (페이지네이션)
    paginator = PostPageNumberPagination()

    page = paginator.paginate_queryset(popular_posts_data, request)

    serializer = PostSimpleSerializer(page, many=True)

    return paginator.get_pages(serializer.data)

from board.models.popular_post_models import PopularPost
from board.models.board_models import Board
from board.services.post_list import PostPageNumberPagination
from board.serializers.post_serializer import PostSimpleSerializer


def get_popular_board_list(request):
    # PopularPost 객체들의 post까지 불러옴 
    get_popular_posts = PopularPost.objects.select_related('post').filter(post__is_blocked=False, post__is_deleted=False).order_by('-popular_at')
    popular_posts_data = [popular_post.post for popular_post in get_popular_posts]


    # 아래서부터는 정섭오빠 코드 참고함 (페이지네이션)
    paginator = PostPageNumberPagination()

    page = paginator.paginate_queryset(popular_posts_data, request)

    serializer = PostSimpleSerializer(page, many=True)

    return paginator.get_pages(serializer.data)
from ..serializers import PostSimpleSerializer
from ..models import Board, Post
from rest_framework.permissions import *
from django.db.models import Q
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
    

"""
게시반 별 리스트 반환 (페이지네이션으로 대체 예정)
"""
def unpaginated_post_list(request, board_id):
        board = Board.objects.get(pk = board_id)
        posts = board.post.filter(is_blocked = False, is_deleted = False).order_by('-created_at')
        if board_id != 6:
            serializer = PostSimpleSerializer(posts, many = True)
            return serializer.data
        paginator = PostPageNumberPagination()
        page = paginator.paginate_queryset(posts, request)

        serializer = PostSimpleSerializer(page, many = True)
        return paginator.get_pages(serializer.data)


"""
게시판별 리스트를 페이지네이션 하여 반환
"""
def paginated_post_list(request, board_id):
    board = Board.objects.get(pk = board_id)
    posts = board.post.filter(is_blocked = False, is_deleted = False).order_by('-created_at')
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)


"""
특정 게시판의 최근 게시물 5개를 반환
"""
def recent_posts_in_board(board_id):
    latest_posts = Post.objects.filter(Q(board__pk = board_id)&Q(is_blocked = False)&Q(is_deleted = False)).order_by('-created_at')[:5]
    serializer = PostSimpleSerializer(latest_posts, many = True)
    return serializer.data


"""
전체 게시판의 최근 게시물 3개를 반환
"""
def recent_posts_in_all_boards():
    latest_posts = Post.objects.exclude(Q(board__pk = 6)|Q(is_blocked = True)|Q(is_deleted = True)).order_by('-created_at')[:3]
    serializer = PostSimpleSerializer(latest_posts, many = True)
    return serializer.data


"""
내가 쓴 게시글 반환 (페이지네이션으로 대체 예정)
"""
def my_posts(user):
    posts = user.post.filter(Q(is_deleted = False)&Q(is_blocked = False)).order_by('-created_at')
    serializer = PostSimpleSerializer(posts, many = True)
    return serializer.data


"""
내가 댓글을 쓴 게시글 반환 (페이지네이션으로 대체 예정)
"""
def my_comments(user):
    posts = Post.objects.filter(comment__member=user, is_deleted=False, is_blocked=False).prefetch_related('comment__post').distinct().order_by('-created_at')
    serializer = PostSimpleSerializer(posts, many = True)
    return serializer.data


"""
내가 쓴 게시글을 페이지네이션 하여 반환
"""
def paginated_my_posts_list(request, user):
    posts = user.post.filter(Q(is_deleted = False)&Q(is_blocked = False)).order_by('-created_at')
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)


"""
내가 댓글을 쓴 게시글을 페이지네이션하여 반환
"""
def paginated_my_comments(request, user):
    posts = Post.objects.filter(comment__member=user, is_deleted=False, is_blocked=False).prefetch_related('comment__post').distinct().order_by('-created_at')
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)
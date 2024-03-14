from ..serializers import PostSimpleSerializer
from ..models import Post
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
검색어 리스트로 쿼리 생성
"""
def build_search_query(word_list):
    query = Q()

    for keyword in word_list: # Q 객체에 검색어 추가
        query |= Q(body__icontains=keyword) | Q(title__icontains=keyword)
    
    return query


"""
하나의 게시판에서 검색
"""
def search_post_in_board(word_list, board_id):
    posts = Post.objects.filter(Q(board = board_id) & build_search_query(word_list)).order_by('-created_at')
    
    return PostSimpleSerializer(posts, many = True).data


"""
모든 게시판에서 검색
"""
def search_post_in_all_boards(word_list):
    posts = Post.objects.filter(build_search_query(word_list)).order_by('-created_at')

    return PostSimpleSerializer(posts, many = True).data


"""
특정 게시판의 검색 결과를 페이지네이션하여 반환
"""
def paginate_and_search_post_in_board(request, word_list, board_id):
    posts = Post.objects.filter(Q(board = board_id) & build_search_query(word_list)).order_by('-created_at')
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)
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


def search_post_by_board_id_and_dorm_id(request, word_list, board_id):
    ## 전체 게시판(1~7)에 대하여 검색
    if board_id == 0:
      query = Q(build_search_query(word_list)
                &Q(is_blocked = False)
                &Q(is_deleted = False)
                &(~Q(board_id = 6))
                &(
                    Q(dorm = request.user.dorm_id)|Q(board_id = 7))
                )
    ## 전체 기숙사 게시판(7)에 대하여 검색
    elif board_id == 7:
        query = (Q(build_search_query(word_list))
                 &Q(is_blocked = False)
                 &Q(is_deleted = False)
                 &Q(board_id = 7))
    ## 특정 게시판에 대하여 검색(1~6)
    else:
        query = Q(build_search_query(word_list)
                  &Q(is_blocked = False)
                  &Q(is_deleted = False)
                  &(
                      Q(dorm = request.user.dorm_id)&Q(board_id = board_id))
                  )

    posts = Post.objects.filter(query).order_by('-created_at')

    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)




"""
deprecated
하나의 게시판에서 검색
"""
def search_post_in_board(word_list, board_id):
    posts = Post.objects.filter(Q(board = board_id) & build_search_query(word_list)).order_by('-created_at')
    
    return PostSimpleSerializer(posts, many = True).data


"""
deprecated
모든 게시판에서 검색
"""
def search_post_in_all_boards(word_list):
    posts = Post.objects.filter(build_search_query(word_list)).order_by('-created_at')

    return PostSimpleSerializer(posts, many = True).data


"""
deprecated
특정 게시판의 검색 결과를 페이지네이션하여 반환
"""
def paginate_and_search_post_in_board(request, word_list, board_id):
    posts = Post.objects.filter(Q(board = board_id) & build_search_query(word_list)).order_by('-created_at')
    paginator = PostPageNumberPagination()
    page = paginator.paginate_queryset(posts, request)

    serializer = PostSimpleSerializer(page, many = True)

    return paginator.get_pages(serializer.data)
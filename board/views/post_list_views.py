from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


class PostPageNumberPagination(PageNumberPagination):
    """
    페이지네이션 클래스
    """
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            ('postList', data),
        ]))


class PostListView(APIView):
    """
    게시판별 리스트 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        board = Board.objects.get(pk = board_id)
        posts = board.post.filter(is_blocked = False, is_deleted = False).order_by('-created_at')
        if board_id != 6:
            serializer = PostSimpleSerializer(posts, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        paginator = PostPageNumberPagination()
        page = paginator.paginate_queryset(posts, request)

        serializer = PostSimpleSerializer(page, many = True)
        return paginator.get_paginated_response(serializer.data)
    

class FreeBoardSimpleView(APIView):
    """
    특정/전체 게시판의 최근 게시물을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        if board_id != 0: # 특정 게시판에 대하여
            latest_posts = Post.objects.filter(Q(board__pk = board_id)&Q(is_blocked = False)&Q(is_deleted = False)).order_by('-created_at')[:5]
        else: # 전체 게시판에 대하여
            latest_posts = Post.objects.exclude(Q(board__pk = 6)|Q(is_blocked = True)|Q(is_deleted = True)).order_by('-created_at')[:3]
        serializer = PostSimpleSerializer(latest_posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class MyPostView(APIView):
    """
    마이페이지에서 내가 쓴 게시글을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = request.user.post.filter(Q(is_deleted = False)&Q(is_blocked = False)).order_by('-created_at')
        serializer = PostSimpleSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class MyCommentView(APIView):
    """
    내가 댓글을 쓴 게시글들을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(comment__member=request.user, is_deleted=False, is_blocked=False).prefetch_related('comment__post').distinct().order_by('-created_at')
        serializer = PostSimpleSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
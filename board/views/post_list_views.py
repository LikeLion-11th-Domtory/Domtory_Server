from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from django.db.models import Q


class PostListView(APIView):
    """
    게시판별 리스트 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        posts = Post.objects.filter(board = board_id, is_blocked = False, is_deleted = False).order_by('-created_at')
        serializer = PostSimpleSerializer(posts, many = True)
        Board.objects.get(pk = board_id)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

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
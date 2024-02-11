from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsOwnerOrReadOnly


class PostListView(APIView):
    """
    게시판별 리스트 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        posts = Post.objects.filter(board_id = board_id, is_blocked = False, is_deleted = False).order_by('-created_at')
        serializer = PostSimpleSerializer(posts, many = True)
        board = Board.objects.get(pk = board_id)
        res = {
            "msg" : f"{board.name}의 게시글 목록",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
    

class FreeBoardSimpleView(APIView):
    """
    자유게시판 상위 5개
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_posts = Post.objects.filter(board_id = 1, is_blocked = False, is_deleted = False).order_by('-created_at')[:5]
        serializer = PostSimpleSerializer(latest_posts, many = True)
        res = {
            "msg" : "자유게시판 최근 5개 게시물 반환",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
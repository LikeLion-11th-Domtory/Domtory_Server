from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers import PostResponseSerializer
from ..models import Post
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from ..services import (create_post,
                        update_post,
                        delete_post,)

class PostCreateView(APIView):
    """
    게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        if board_id == 6:
            res = {
                "detail": "자율회 게시글 작성 API를 사용해주세요."
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
        response = create_post(request, board_id)
        return Response(response, status = status.HTTP_201_CREATED)


class PostUpdateView(APIView):
    """
    게시글 수정 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, post_id):
        post = Post.objects.get(pk = post_id)
        self.check_object_permissions(request, post)
        response = update_post(request, post)
        return Response(response, status = status.HTTP_200_OK)


class PostDeleteView(APIView):
    """
    게시글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, post_id):
        post = Post.objects.get(pk = post_id)
        self.check_object_permissions(request, post)
        response = delete_post(post)
        return Response(response, status = status.HTTP_204_NO_CONTENT)


class PostDetailView(APIView):
    """
    게시글 디테일 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        serializer = PostResponseSerializer(post, context = {'request' : request})
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class CouncilPostCreateView(APIView):
    """
    자율회 게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def post(self, request):
        response = create_post(request, 6)
        return Response(response, status = status.HTTP_201_CREATED)
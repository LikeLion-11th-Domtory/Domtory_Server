from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsOwnerOrReadOnly


class PostCreateView(CreateAPIView):
    """
    게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = PostRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
            user = self.request.user
            post = serializer.save(member = user)


class PostUpdateDeleteView(APIView):
    """
    게시글 수정 및 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = PostRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        serializer = PostRequestSerializer(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "msg" : "게시글 수정 성공",
                "data" : PostResponseSerializer(post).data
            }
            return Response(res, status = status.HTTP_200_OK)
        else:
            res = {
                "msg" : "유효하지 않는 요청 정보"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        post.delete()
        res = {
            "msg" : "게시글 삭제 완료"
        }
        return Response(res, status = status.HTTP_201_CREATED)


class PostDetailView(RetrieveAPIView):
    """
    게시글 디테일 뷰
    """
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PostResponseSerializer
    permission_classes = [IsAuthenticated]
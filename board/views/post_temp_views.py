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
from PIL import Image
from io import BytesIO
from utils.s3 import S3Connect
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile
import mimetypes


class PostCreateView(APIView):
    """
    게시글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        serializer = PostRequestSerializer(data = request.data)
        if serializer.is_valid():
            board = get_object_or_404(Board, pk = board_id)
            post = serializer.save(member = request.user, board = board)

            res = {
                "msg" : "게시글 작성 성공",
                "data" : PostResponseSerializer(post).data
            }
            return Response(res, status = status.HTTP_201_CREATED)
        res = {
            "msg" : "게시글 작성 실패",
            "data" : serializer.errors
        }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)
        

    

class PostDetailView(APIView):
    """
    게시글 상세정보 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        serializer = PostResponseSerializer(post)
        res = {
            "msg" : "게시글 상세정보 불러오기 성공",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
    
    
class PostUpdateDeleteView(APIView):
    """
    게시글 수정 및 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        self.check_object_permissions(request, post)
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
                "msg" : "유효하지 않은 데이터"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        post.is_deleted = True
        post.save()
        res = {
            "msg" : "게시글 삭제 완료"
        }
        return Response(res, status = status.HTTP_201_CREATED)
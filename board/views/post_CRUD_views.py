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
    게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        board = Board.objects.get(pk = board_id)
        serializer = PostRequestSerializer(data = request.data)
        if serializer.is_valid():
            post = serializer.save(member = request.user, board = board)

            image_request_serializer = ImageRequestSerializer(data = request.data)
            image_request_serializer.is_valid(raise_exception=True)
            image_data = image_request_serializer.validated_data
            image_list = image_data.get('images')
            if image_list:
                try:
                    self.upload_image(post, image_list)
                    return Response(PostResponseSerializer(post).data, status = status.HTTP_201_CREATED)
                except:
                    post.delete()
                    res = {
                        "msg" : "이미지 업로드 실패"
                    }
                    return Response(res, status = status.HTTP_400_BAD_REQUEST)
            return Response(PostResponseSerializer(post).data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def upload_image(self, post, image_list):
        s3 = S3Connect()
        for i in range(0, len(image_list)):
            image = Image.open(image_list[i])
            image = image.convert('RGB')

            image.thumbnail((2000, 2000))
            buffer = BytesIO()
            image.save(buffer, format = 'JPEG', quality = 80)
            image_data = buffer.getvalue()

            key = f"{post.board.name}_{post.pk}_{uuid.uuid4().hex}.jpeg"
            image_url = s3.upload_to_s3(image_data = image_data, key = key, content_type = 'image/jpeg')
            
            PostImage(post = post, image_url = image_url).save()
            
            if i == 0:
                post.thumbnail_url = image_url
                post.save()


class PostUpdateView(APIView):
    """
    게시글 수정 뷰
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = PostRequestSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        self.check_object_permissions(request, post)
        post_serializer = PostRequestSerializer(post, data = request.data)
        image_serializer = ImageRequestSerializer(data = request.data)
        if not post_serializer.is_valid():
            {
                "msg" : "유효하지 않은 게시글 형식"
            }
        if not image_serializer.is_valid():
            {
                "msg" : "유효하지 않은 이미지 형식"
            }
        
        deleted_images = request.data['deleted_images']
        if deleted_images:
            for img_id in deleted_images:
                get_object_or_404(PostImage, pk = img_id).delete()

        image_data = image_serializer.validated_data
        image_list = image_data.get('images')
        if image_list:
            try:
                self.upload_image(post, image_list)
                # post.save()
                first_image = post.post_image.first()
                if first_image:
                    post.thumbnail_url = first_image.image_url
                else:
                    post.thumbnail_url = None
                post.save()
                return Response(PostResponseSerializer(post).data, status = status.HTTP_200_OK)
            except:

                res = {
                    "msg" : "이미지 업로드 실패"
                }
                return Response(res, status = status.HTTP_400_BAD_REQUEST)
        first_image = post.post_image.first()
        if first_image:
            post.thumbnail_url = first_image.image_url
        else:
            post.thumbnail_url = None
        post.save()
        return Response(PostResponseSerializer(post).data, status = status.HTTP_200_OK)
        

    def upload_image(self, post, image_list):
        s3 = S3Connect()
        for i in range(0, len(image_list)):
            image = Image.open(image_list[i])
            image = image.convert('RGB')

            image.thumbnail((2000, 2000))
            buffer = BytesIO()
            image.save(buffer, format = 'JPEG', quality = 80)
            image_data = buffer.getvalue()

            key = f"{post.board.name}_{post.pk}_{uuid.uuid4().hex}.jpeg"
            image_url = s3.upload_to_s3(image_data = image_data, key = key, content_type = 'image/jpeg')
            
            PostImage(post = post, image_url = image_url).save()

class PostDeleteView(APIView):
    """
    게시글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        post.is_deleted = True
        post.save()
        res = {
            "msg" : "게시글 삭제 완료"
        }
        return Response(res, status = status.HTTP_204_NO_CONTENT)


class PostDetailView(APIView):
    """
    게시글 디테일 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, requset, post_id):
        post = get_object_or_404(Post, pk = post_id)
        serializer = PostResponseSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
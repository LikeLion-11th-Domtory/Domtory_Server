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
            post = serializer.save(member_id = request.user, board_id = board)

            image_request_serializer = ImageRequestSerializer(data = request.data)
            image_request_serializer.is_valid(raise_exception=True)
            image_data = image_request_serializer.validated_data
            image_list = image_data.get('images')
            if image_list:
                
                res = {
                    "msg" : "게시글 작성 성공",
                    "data" : PostResponseSerializer(post).data
                    # "data" : image_list[0].content_type
                }
                return Response(res, status = status.HTTP_201_CREATED)
                # except:
                #     post.delete()
                #     res = {
                #         "msg" : "유효하지 않은 이미지"
                #     }
                #     return Response(res, status = status.HTTP_400_BAD_REQUEST)
        res = {
            "msg" : "유효하지 않은 게시글 데이터"
        }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)

    def upload_image(self, post, image_list):
        s3 = S3Connect()
        for i in range(0, len(image_list)):
            image = Image.open(image_list[i])
            image_thumbnail = image.copy()
            if i == 0:
                self.post_thumbnail(post, image_thumbnail, s3)
            image_format = image.format

            image = image.convert('RGB')
            image.thumbnail((2000, 2000))

            image_io = BytesIO()
            image.save(image_io, format = 'JPEG', quality = 85)

            uuid_key = uuid.uuid4().hex
            image_file = InMemoryUploadedFile(image_io, None, uuid_key, 'image/jpeg', image_io.tell(), None)

            image_file.content_type = 'image/jpeg'
            key = f"{post.board_id.name}_{post.pk}_{uuid_key}.jpeg"
            s3.upload_to_s3(image_file, key)


    def post_thumbnail(self, post, image, s3):
            image = image.convert('RGB')
            image.thumbnail((1000, 1000))

            image_io = BytesIO()
            image.save(image_io, format = 'JPEG', quality = 85)

            uuid_key = uuid.uuid4().hex
            image_file = InMemoryUploadedFile(image_io, None, uuid_key, 'image/jpeg', image_io.tell(), None)

            image_file.content_type = 'image/jpeg'
            key = f"{post.board_id.name}_{post.pk}_{uuid_key}.jpeg"
            s3.upload_to_s3(image_file, key)






class PostUpdateDeleteView(APIView):
    """
    게시글 수정 및 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = PostRequestSerializer
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
        res = {
            "msg" : "게시글 삭제 완료"
        }
        return Response(res, status = status.HTTP_201_CREATED)


class PostDetailView(APIView):
    """
    게시글 디테일 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, requset, post_id):
        post = get_object_or_404(Post, pk = post_id)
        serializer = PostResponseSerializer(post)
        res = {
            "msg" : "게시글 상세정보",
            "data" : serializer.data
        }
        return Response(res, status = status.HTTP_200_OK)
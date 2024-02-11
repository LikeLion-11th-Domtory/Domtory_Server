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
from PIL import Image
from io import BytesIO
from utils.s3 import S3Connect
import uuid


class ImageUploadView(APIView):
    """
    이미지 업로드 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        self.check_object_permissions(request, post)

        image_file = request.FILES['image']
        
        ## 이미지 압축
        image = Image.open(image_file)
        image = image.convert('RGB')
        s3 = S3Connect()
        
        if request.data.get('thumbnail') == "true":
            self.make_thumbnail(image, post)

        size = (2000, 2000)
        image.thumbnail(size)

        buffer = BytesIO()
        image.save(buffer, format = 'JPEG', quality = 85)
        image_data = buffer.getvalue()
        

        ## s3에 등록할 key 생성
        key = f"{post.board_id.name}_{post.pk}_{uuid.uuid4().hex}.jpeg"

        ## s3에 이미지 저장
        s3 = S3Connect()
        image_url = s3.upload_to_s3(image_data, key)

        PostImage(post_id = post, image_url = image_url).save()

        res = {
            "msg" : "이미지 업로드 성공",
            "data" : PostResponseSerializer(post).data
        }
        
        return Response(res, status = status.HTTP_201_CREATED)

    def make_thumbnail(image, post):
        """
        게시글 썸네일 등록 메소드
        """
        image.thumbnail((1000, 1000))

        buffer = BytesIO()
        image.save(buffer, format = 'JPEG', quality = 85)
        image_data = buffer.getvalue()

        key = f"{post.board_id.name}_{post.pk}_thumbnail.jpeg"

        s3 = S3Connect()
        post.thumbnail_url = s3.upload_to_s3(image_data, key)
        post.save()
    

class ImageDeleteView(APIView):
    """
    이미지 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    
    def delete(self, request, image_id):
        image = get_object_or_404(PostImage, pk = image_id)
        self.check_object_permissions(request, image.post_id)

        s3 = S3Connect()
        try:
            s3.delete_object(image.image_url)
            image.delete()
            res = {
                "msg" : "성공적으로 이미지 삭제"
            }
            return Response(res, status = status.HTTP_204_NO_CONTENT)
        except:
            res = {
                "msg" : "이미지 삭제 실패"
            }
            return Response(res, status = status.HTTP_400_BAD_REQUEST)
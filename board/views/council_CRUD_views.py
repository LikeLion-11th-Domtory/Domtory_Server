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


class CouncilPostCreateView(APIView):
    """
    자율회 게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        board = Board.objects.get(pk = 6)
        serializer = PostRequestSerializer(data = request.data)
        if serializer.is_valid():
            post = serializer.save(member = request.user, board = board)
            if 'images' not in request.data:
                return Response(PostResponseSerializer(post).data, status = status.HTTP_201_CREATED)

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

            key = f"{post.board.name}/{post.pk}_{uuid.uuid4().hex}.jpeg"
            image_url = s3.upload_to_s3(image_data = image_data, key = key, content_type = 'image/jpeg')
            
            PostImage(post = post, image_url = image_url).save()
            
            if i == 0:
                post.thumbnail_url = image_url
                post.save()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsStaffOrReadOnly
from utils.s3 import S3Connect
from push.tasks import send_push_notification_handler

class CouncilPostCreateView(APIView):
    """
    자율회 게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def post(self, request):
        board = Board.objects.get(pk = 6)
        serializer = PostRequestSerializer(data = request.data)
        if serializer.is_valid():
            post = serializer.save(member = request.user, board = board)
            send_push_notification_handler.delay('post-notification-event', post_id=post.id)
            if 'images' not in request.data:
                return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_201_CREATED)

            image_request_serializer = ImageRequestSerializer(data = request.data)
            image_request_serializer.is_valid(raise_exception=True)
            image_data = image_request_serializer.validated_data
            image_list = image_data.get('images')
            if image_list:
                try:
                    s3 = S3Connect()
                    s3.upload_resized_image(post, image_list)
                    return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_201_CREATED)
                except:
                    post.delete()
                    res = {
                        "msg" : "이미지 업로드 실패"
                    }
                    return Response(res, status = status.HTTP_400_BAD_REQUEST)
            return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
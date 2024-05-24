from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from board.models import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from board.permissions import IsStaffOrReadOnly
from board.models import Post, Comment
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class CreateReportView(APIView):

    def post(self, request, target_type, target_id):
        if target_type == "post":
            target = Post.objects.get(pk=target_id)
            data = request.data.copy()
            data['post'] = target_id

        elif target_type == "comment":
            target = Comment.objects.get(pk=target_id)
            data = request.data.copy()
            data['comment'] = target_id

        elif target_type == "message":
            target = Message.objects.get(pk=target_id)
            data = request.data.copy()
            data['message'] = target_id
        
        serializer = ReportSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # 람다 서버에 보내서 욕설 체크
            dataset = {
                "target" : target.body,
                'target_id' : target.id,
                'table' : target_type,
                'report_id' : serializer.data['id']
            }
            requests.post('https://8ufbqa4zl8.execute-api.ap-northeast-2.amazonaws.com/prod', json=dataset)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class IsBlockedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    @swagger_auto_schema(request_body=IsBlindRequestSerializer, responses={"200": ""})
    def post(self, request):
        """
        특정 게시글/게시판을 block 시키는 view 입니다.
        type에는 종류에 따라서 'post' 아니면 'comment'가 들어갑니다.
        """
        is_blind_request_serializer = IsBlindRequestSerializer(data=request.data)
        is_blind_request_serializer.is_valid(raise_exception=True)
        is_blind_data = is_blind_request_serializer.validated_data

        post_or_comment_id = is_blind_data.get('post_or_comment_id')
        type = is_blind_data.get('type')

        if type == "comment":
            target_comment = get_object_or_404(Comment, id=post_or_comment_id)
            target_comment.is_blocked = True
            target_comment.save(update_fields=['is_blocked'])

        elif type == "post":
            target_post = get_object_or_404(Post, id=post_or_comment_id)
            target_post.is_blocked = True
            target_post.save(update_fields=['is_blocked'])
        else:
            return TypeError
        return Response(status=status.HTTP_200_OK)
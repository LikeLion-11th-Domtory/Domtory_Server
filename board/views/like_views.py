from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *

from board.services.post_like import *
from board.services.comment_like import *


class PostLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        response = create_post_like(request, post_id)
        return Response(response, {"detail": "이 글을 공감하였습니다."}, status=status.HTTP_200_OK)
    

class CommentLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        response = create_comment_like(request, post_id)
        return Response(response, {"detail": "이 댓글을 공감하였습니다."}, status=status.HTTP_200_OK)
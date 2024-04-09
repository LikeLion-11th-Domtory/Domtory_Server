from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..services import (create_comment,
                        delete_comment,
                        create_reply,)

class CommentCreateView(APIView):
    """
    댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        response = create_comment(request, post_id)
        return Response(response, status = status.HTTP_201_CREATED)
        

class CommentDeleteView(APIView):
    """
    댓글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        response = delete_comment(request, comment_id)
        return Response(response, status = status.HTTP_204_NO_CONTENT)


class ReplyCreateView(APIView):
    """
    대댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        response = create_reply(request, comment_id)
        return Response(response, status = status.HTTP_201_CREATED)
    

class ReplyDeleteView(APIView):
    """
    대댓글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, reply_id):
        response = delete_comment(request, reply_id)
        return Response(response, status = status.HTTP_204_NO_CONTENT)
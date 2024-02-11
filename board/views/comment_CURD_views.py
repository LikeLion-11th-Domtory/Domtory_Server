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

class CommentCreateView(APIView):
    """
    댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        serializer = CommentRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(post = post, member = request.user)
            res = {
                "msg" : "성공적으로 댓글 작성",
                "data" : PostResponseSerializer(post).data
            }
            return Response(res, status = status.HTTP_201_CREATED)
        res = {
            "msg" : "댓글 작성 실패",
            "data" : serializer.errors
        }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)
        

class CommentDeleteView(APIView):
    """
    댓글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk = comment_id)
        post = comment.post
        self.check_object_permissions(request, comment)

        comment.is_deleted = True
        comment.save()
        
        res = {
            "msg" : "댓글 삭제 성공",
            "data" : PostResponseSerializer(post).data
        }
        return Response(res, status = status.HTTP_201_CREATED)



class ReplyCreateView(APIView):
    """
    대댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk = comment_id)
        post = comment.post
        serializer = ReplyRequestSerializer(data = request.data)
        if serializer.is_valid():
            reply = serializer.save(parent = comment, post = post, member = request.user)
            post = reply.parent.post
            res = {
                "msg" : "성공적으로 대댓글 작성",
                "data" : PostResponseSerializer(post).data
            }
            return Response(res, status = status.HTTP_201_CREATED)
        res = {
            "msg" : "대댓글 작성 실패",
            "data" : serializer.errors
        }
        return Response(res, status = status.HTTP_400_BAD_REQUEST)
    

class ReplyDeleteView(APIView):
    """
    대댓글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, reply_id):
        reply = get_object_or_404(Comment, pk = reply_id)
        post = reply.post
        self.check_object_permissions(request, reply)

        reply.is_deleted = True
        reply.save()

        res = {
            "msg" : "성공적으로 대댓글 삭제",
            "data" : PostResponseSerializer(post).data
        }
        return Response(res, status = status.HTTP_201_CREATED)
        
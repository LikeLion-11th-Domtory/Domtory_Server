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
from push.tasks import send_push_notification_handler

class CommentCreateView(APIView):
    """
    댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.prefetch_related('comment').get(pk = post_id)

        comments = post.comment.all()
        anonymous_number = 0

        if request.user != post.member:
            flag = False

            for comment in comments:
                if comment.member == request.user:
                    anonymous_number = comment.anonymous_number
                    flag = True
                    break
                if anonymous_number < comment.anonymous_number:
                    anonymous_number = comment.anonymous_number

            if flag == False:
                anonymous_number += 1

        
        serializer = CommentRequestSerializer(data = request.data)
        if serializer.is_valid():
            comment = serializer.save(post = post, member = request.user, anonymous_number = anonymous_number)
            post.comment_cnt += 1
            post.save()
            send_push_notification_handler.delay('comment-notification-event', None, comment.id)
            return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

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
        post.comment_cnt -= 1
        post.save()

        return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_204_NO_CONTENT)



class ReplyCreateView(APIView):
    """
    대댓글 생성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        parent = get_object_or_404(Comment, pk = comment_id)
        post = parent.post

        comments = post.comment.all()
        anonymous_number = 0

        if request.user != post.member:
            flag = False

            for comment in comments:
                if comment.member == request.user:
                    anonymous_number = comment.anonymous_number
                    flag = True
                    break
                if anonymous_number < comment.anonymous_number:
                    anonymous_number = comment.anonymous_number

            if flag == False:
                anonymous_number += 1

        serializer = ReplyRequestSerializer(data = request.data)
        if serializer.is_valid():
            reply = serializer.save(parent = parent, post = post, member = request.user, anonymous_number = anonymous_number)
            post.comment_cnt += 1
            post.save()
            send_push_notification_handler.delay('comment-notification-event', None, reply.id)
            return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

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
        post.comment_cnt -= 1
        post.save()
        return Response(PostResponseSerializer(post, context = {'request' : request}).data, status = status.HTTP_204_NO_CONTENT)
        
from django.shortcuts import get_object_or_404
from ..serializers import CommentRequestSerializer, ReplyRequestSerializer
from ..models import Post, Comment
from board.services.post_CRUD import get_post_detail
from rest_framework.permissions import *
from push.tasks import send_push_notification_handler
from utils.exceptions import CommentPermissionError


"""
댓글 작성 메소드
"""
def create_comment(request, post_id):
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
        comment = serializer.save(post = post, member = request.user, anonymous_number = anonymous_number, dorm = request.user.dorm)
        post.comment_cnt += 1
        post.save()
        # send_push_notification_handler.delay('comment-notification-event', None, comment.id)
        response = get_post_detail(request, post.id)
        return response
    return serializer.errors


"""
댓글 삭제 메소드
"""
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id = comment_id)
    if comment.member != request.user:
        raise CommentPermissionError
    
    post = comment.post
    comment.is_deleted = True
    comment.save()
    if post.comment_cnt > 0:
        post.comment_cnt -= 1
        post.save()
    response = get_post_detail(request, post.pk)
    return response


"""
대댓글 작성 메소드
"""
def create_reply(request, comment_id):
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
        reply = serializer.save(parent = parent, post = post, member = request.user, anonymous_number = anonymous_number, dorm = request.user.dorm)
        post.comment_cnt += 1
        post.save()
        # send_push_notification_handler.delay('comment-notification-event', None, reply.id)
        response = get_post_detail(request, post.pk)
        return response
    return serializer.errors
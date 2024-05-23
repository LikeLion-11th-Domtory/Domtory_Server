from django.db import models

from board.models import Post
from member.domains import Member


class MessageRoom(models.Model):
    """
    쪽지 시작점 참고를 위한 모델
    """
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL, verbose_name='쪽지 시작점 게시글', related_name='message_post')
    board = models.CharField(max_length=60, default="", verbose_name='쪽지 시작점 게시글의 게시판')
    post_title = models.CharField(max_length=90, default="", verbose_name='쪽지 시작점 게시글 제목')
    receiver_anonymous_num = models.IntegerField(verbose_name='최초수신자 익명 숫자') # 0이면 게시글 작성자, 1 이상이면 댓글 작성자
    first_sender = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='최초발신자', related_name='first_message_sender')
    first_receiver = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='최초수신자',
                                 related_name='first_message_receiver')


class Message(models.Model):
    """
    쪽지 모델
    """
    message_room = models.ForeignKey(MessageRoom, null=True, on_delete=models.SET_NULL, verbose_name='쪽지방', related_name='message_room')
    sender = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='송신자', related_name='message_sender')
    receiver = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='수신자', related_name='message_receiver')
    body = models.TextField(default="", verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='전송일시')
    is_read = models.BooleanField(default=False)
    is_deleted_send = models.BooleanField(default=False)
    is_deleted_recv = models.BooleanField(default=False)
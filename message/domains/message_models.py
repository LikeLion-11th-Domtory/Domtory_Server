from django.db import models
from member.domains import Member


class Message(models.Model):
    """
    쪽지 모델
    """
    send_id = models.ForeignKey(Member, null=False, on_delete=models.CASCADE, verbose_name='송신자', related_name='message_sender')
    recv_id = models.ForeignKey(Member, null=False, on_delete=models.CASCADE, verbose_name='수신자', related_name='message_receiver')
    body = models.TextField(default="", verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='전송일시')
    is_read = models.BooleanField(default=False)
    is_deleted_send = models.BooleanField(default=False)
    is_deleted_recv = models.BooleanField(default=False)
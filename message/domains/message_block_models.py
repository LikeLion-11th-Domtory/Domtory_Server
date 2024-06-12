from django.db import models

from member.domains import Member


class MessageBlock(models.Model):
    """
    쪽지 차단 목록 모델
    """
    requester = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='발신자', related_name='block_sender')
    target = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, verbose_name='수신자', related_name='block_receiver')

    class Meta:
        db_table = 'message_block'
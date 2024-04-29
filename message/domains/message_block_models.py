from django.db import models

from member.domains import Member


class MessageBlock(models.Model):
    """
    쪽지 차단 목록 모델
    """
    req_id = models.ForeignKey(Member, null=False, on_delete=models.CASCADE, verbose_name='발신자', related_name='block_sender')
    tar_id = models.ForeignKey(Member, null=False, on_delete=models.CASCADE, verbose_name='수신자', related_name='block_receiver')

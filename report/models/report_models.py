from django.db import models
from board.models import Comment, Post
from message.domains.message_models import Message
from member.models import Member


# Create your models here.

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ("WAITING", "검사 대기"),
        ("PENDING", "관리자 확인 대기"),
        ("VALID", "유효한 신고"),
        ("INVALID", "유효하지 않은 신고")
    )
    MEMBER_BLOCK_CHOICES = (
        (0, '정지하지 않음'),
        (3, '3일 정지'),
        (7, '7일 정지'),
        (30, '30일 정지')
    )
    status = models.CharField(choices=REPORT_TYPE_CHOICES, default="WAITING", max_length=10)
    reported_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.ForeignKey(Message, null=True, blank=True, on_delete=models.SET_NULL)
    member_status = models.IntegerField(choices=MEMBER_BLOCK_CHOICES, default=0)

    def __str__(self):
        if self.post:
            return f"게시글 신고 : {self.post.body}"
        elif self.comment:
            return f"댓글 신고 : {self.comment.body}"
        elif self.message:
            return f"쪽지 신고 : {self.message.body}"

    class Meta:
        db_table = 'report'



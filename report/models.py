from django.db import models
from board.models import Comment, Post

# Create your models here.

class Report(models.Model):
    class ReportType(models.TextChoices):
        WAITING = "WAITING", "대기"
        PENDING = "PENDING", "수동검사대기"
        VALID = "VALID", "욕설있음"
        INVALID = "INVALID", "욕설없음"
    status = models.CharField(choices=ReportType.choices, default="WAITING", max_length=10)
    reported_at = models.DateTimeField(auto_now_add=True)
    # report_type = 
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'report'

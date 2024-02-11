from django.db import models
# from borad import Comment, Post

# Create your models here.

class Report(models.Model):
    class ReportType(models.TextChoices):
        WAITING = "WAITING", "대기"
        PENDING = "PENDING", "수동검사대기"
        VALID = "VALID", "욕설있음"
        INVALID = "INVALID", "욕설없음"
    status = models.CharField(choices=ReportType.choices, default="WAITING")
    reported_at = models.DateTimeField(auto_now_add=True)
    # report_type = 
    post = models.ForeignKey(Post, null=True)
    comment = models.ForeignKey(Comment, null=True)

from django.db import models
from board.models import Comment, Post

# Create your models here.

class Report(models.Model):
    class ReportType(models.TextChoices):
        WAITING = "WAITING", "waiting"
        PENDING = "PENDING", "pending"
        VALID = "VALID", "valid"
        INVALID = "INVALID", "invalid"
    status = models.CharField(choices=ReportType.choices, default="WAITING", max_length=10)
    reported_at = models.DateTimeField(auto_now_add=True)
    # report_type = 
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'report'

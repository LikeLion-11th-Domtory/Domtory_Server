from django.db import models
from .post_models import Post
from member.domains.member import Member

class Comment(models.Model):
    """
    댓글 모델
    """
    member = models.ForeignKey(Member, null = False, on_delete = models.CASCADE, related_name = 'comment')
    post = models.ForeignKey(Post, null = False, blank = True, on_delete = models.CASCADE, related_name = 'comment')
    parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.PROTECT, related_name = 'reply')
    body = models.TextField(default = "", null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    is_blocked = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)

    def __str__(self):
        return self.body

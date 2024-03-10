from django.db import models
from board.models.comment_models import Comment
from member.domains.member import Member

class CommentMemberLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'like')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name = 'like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_member_like'
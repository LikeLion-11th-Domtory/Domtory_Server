from django.db import models
from board.models.post_models import Post
from member.domains.member import Member

class PostMemberLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_member_like'
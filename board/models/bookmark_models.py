from django.db import models
from member.domains.member import Member
from board.models.post_models import Post

class PostMemberBookmark(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_member_bookmark'
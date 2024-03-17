from django.db import models
from board.models.comment_models import Comment
from member.domains.member import Member
from board.models.post_models import Post


class PostMemberLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_member_like'

        

class CommentMemberLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = 'like')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name = 'like')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_member_like'
from django.db import models
from .post_models import Post
from member.domains.member import Member

class Comment(models.Model):
    """
    댓글 모델
    """
    member = models.ForeignKey(Member, null = False, on_delete = models.CASCADE, verbose_name = '작성자', related_name = 'comment')
    post = models.ForeignKey(Post, null = False, blank = True, on_delete = models.CASCADE, verbose_name = '게시글', related_name = 'comment')
    parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.PROTECT, verbose_name = '댓글', related_name = 'reply')
    body = models.TextField(default = "", verbose_name = '내용', null = False)
    anonymous_number = models.IntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = '작성일시')
    is_blocked = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    likes_cnt = models.IntegerField(default = 0, null = True, verbose_name = "좋아요 수")

    def __str__(self):
        return self.body
    
    class Meta:
        db_table = 'comment'
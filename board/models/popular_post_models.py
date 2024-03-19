from django.db import models
from board.models.post_models import Post


class PopularPost(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    popular_at = models.DateTimeField(auto_now_add=True, verbose_name = "인기게시물 등록 시간")

    class Meta:
        db_table = 'popular_post'
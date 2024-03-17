from django.db import models
from board.models.post_models import Post


class PopularPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    popular_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'popular_post'
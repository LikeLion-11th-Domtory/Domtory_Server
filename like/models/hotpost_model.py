from django.db import models
from board.models.post_models import Post


class HotPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hot_at = models.DateTimeField(auto_now_add=True)
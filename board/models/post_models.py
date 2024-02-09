from django.db import models
from .board_models import Board
from member.domains.member import Member

class Post(models.Model):
    """
    게시글 모델
    """
    member = models.ForeignKey(Member, null = False, on_delete = models.CASCADE, related_name = 'post')
    board = models.ForeignKey(Board, null = False, on_delete = models.CASCADE, related_name = 'post')
    title = models.CharField(max_length = 90, null = False) # 한글 30글자
    body = models.TextField(default = "")
    created_at = models.DateTimeField(auto_now_add = True)
    is_blocked = models.BooleanField(default = False, blank = True)
    is_deleted = models.BooleanField(default = False, blank = True)
    thumbnail_url = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.title

    def create(self, validated_data):
        # member_id 필드를 request.user로 설정
        validated_data['member'] = self.context['request'].user
        return super().create(validated_data)


class PostImage(models.Model):
    """
    게시글 이미지 모델
    """
    post = models.ForeignKey(Post, null = False, on_delete = models.CASCADE, related_name = 'post_image')
    image_url = models.TextField(null = False)

    def __str__(self):
        return self.image_url
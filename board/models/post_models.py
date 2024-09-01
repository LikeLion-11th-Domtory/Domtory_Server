from django.db import models
from .board_models import Board
from member.domains.member import Member

class Post(models.Model):
    """
    게시글 모델
    """
    member = models.ForeignKey(Member, null = False, on_delete = models.CASCADE, verbose_name = '작성자', related_name = 'post')
    board = models.ForeignKey(Board, null = False, on_delete = models.CASCADE, verbose_name = '게시판', related_name = 'post')
    dorm = models.ForeignKey('dorm.Dorm', null = True, on_delete = models.SET_NULL, verbose_name = '기숙사', related_name = 'post')
    title = models.CharField(max_length = 90, verbose_name = '제목', null = False) # 한글 30글자
    body = models.TextField(default = "", verbose_name = '내용')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = '작성일시')
    comment_cnt = models.IntegerField(default = 0, verbose_name = '댓글 수')
    is_blocked = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    thumbnail_url = models.CharField(null = True, max_length = 255)
    likes_cnt = models.IntegerField(default = 0, null = False, verbose_name = '좋아요 수')
    bookmark_cnt = models.IntegerField(default = 0, null = False, verbose_name = '스크랩 수')

    def __str__(self):
        return self.title

    def create(self, validated_data):
        # member_id 필드를 request.user로 설정
        validated_data['member'] = self.context['request'].user
        return super().create(validated_data)
    
    class Meta:
        db_table = 'post'


class PostImage(models.Model):
    """
    게시글 이미지 모델
    """
    post = models.ForeignKey(Post, null = False, on_delete = models.CASCADE, verbose_name = '게시글', related_name = 'post_image')
    dorm = models.ForeignKey('dorm.Dorm', null = True, on_delete = models.SET_NULL, verbose_name = '기숙사', related_name = 'post_image')
    image_url = models.CharField(null = False, max_length = 255)
    is_deleted = models.BooleanField(default = False)
    is_thumbnail = models.BooleanField(default = False)

    def __str__(self):
        return self.image_url

    
    class Meta:
        db_table = 'post_image'
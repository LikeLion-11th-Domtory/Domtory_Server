from django.db import models

class AdminPushNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('normal', '일반 공지'),
        ('update', '업데이트 알림'),
        ('emergency', '긴급 공지'),
    ]
    id = models.BigAutoField(primary_key=True)
    staff_member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, help_text="제목을 넣어주세요. ex) 돔토리 업데이트 공지사항")
    body = models.CharField(max_length=255, help_text="본문을 넣어주세요. ex) 1.10 버전이 새로 출시 되었으니 업데이트 바라요!")
    created_at = models.DateTimeField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, null=True)
    
    class Meta:
        db_table = 'admin_push_notification'
        verbose_name = "관리자 푸시 알림"
        verbose_name_plural = "관리자 푸시 알림"
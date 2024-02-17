from django.db import models

# Create your models here.

class NoticeList(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    post_id = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    content = models.TextField(null=True)
    images = models.TextField(null=True)
    notice_url = models.CharField(null = True, max_length = 255)
    
    def __str__(self):
        return self.title
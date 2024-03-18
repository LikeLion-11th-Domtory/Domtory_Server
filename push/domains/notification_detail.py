from django.db import models

class NotificationDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.OneToOneField('member.Member', on_delete=models.CASCADE)
    breakfast = models.BooleanField(default=True)
    lunch = models.BooleanField(default=True)
    dinner = models.BooleanField(default=True)
    lightning_post = models.BooleanField(default=True)
    comment = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification_detail'
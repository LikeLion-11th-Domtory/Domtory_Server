from django.db import models

class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_token = models.CharField(max_length=255)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'device'
        unique_together = (('device_token', 'member'),)
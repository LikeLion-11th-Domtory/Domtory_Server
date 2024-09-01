from django.db import models
from dorm.domains import Dorm

class DormitoryPersonalInfo(models.Model):
    dormitory_code = models.CharField(max_length=7)
    room_number = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    dorm = models.ForeignKey(Dorm, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'dormitory_personal_info'
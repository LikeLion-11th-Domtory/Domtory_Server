from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.member_manager import MemberManager
from dorm.domains import Dorm

class Member(AbstractBaseUser, PermissionsMixin):
    objects = MemberManager()
    MEMBER_STATUS_CHOICES = (
        ('PENDING','가입 승인 대기'),
        ('ACTIVE','활동'),
        ('BANNED', '정지'),
        ('WITHDRAWAL', '탈퇴'),
        ('REFUSED','가입 승인 거부')
    )
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=MEMBER_STATUS_CHOICES, default='ACTIVE')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    dorm = models.ForeignKey(Dorm, null=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    last_login = None

    class Meta:
        db_table = 'member'
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from utils.member_manager import MemberManager

class Member(AbstractBaseUser):
    objects = MemberManager()
    MEMBER_STATUS_CHOICES = (
        ('ADMIN_VERIFICATION_PENDING', '관리자 확인 대기'),
        ('ACTIVE','활동'),
        ('BANNED', '정지'),
        ('WITHDRAWAL', '탈퇴')
    )
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    dormitory_code = models.CharField(max_length=255)
    nickname = models.CharField(unique=True, max_length=10)
    phone_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    birthday = models.DateTimeField(max_length=255)
    dormitory_card = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=MEMBER_STATUS_CHOICES, default='ADMIN_VERIFICATION_PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        db_table = 'member'
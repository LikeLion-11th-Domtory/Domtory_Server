import re
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from member.domains import Member
from dorm.domains import Dorm
from django.db.models import Q

ERROR_MESSAGE = {
            'blank': '값을 채워주세요!',
            'required': '값을 채워주세요!'
            }

def validate_password(password):
    password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,13}$"
    password_regex = re.compile(password_reg)

    if not password_regex.match(password):
        raise ValidationError("영문, 숫자, 특수문자를 조합해 6자 이상, 13자 이하 입력해주세요.")
    
def validate_email(email):
    if Member.objects.filter(email=email).exists():
        raise ValidationError("이미 가입된 회원이에요!")
    
    email_reg = r"^[a-zA-Z0-9_-]{4,13}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    email_regex = re.compile(email_reg)

    if not email_regex.match(email):
        raise ValidationError("이메일의 아이디는 4자 이상 13자 이하로 가능하고, 특수 문자는 _와 -만 사용 가능해요.")
    
def validate_nickname(nickname):
    if Member.objects.filter(nickname=nickname).exists():
        raise ValidationError("닉네임이 이미 존재해요! 다른 걸로 부탁해요.")
    
def validate_birthday(birthday):
    birthday_reg = r"^\d{8}$"
    birthday_regex = re.compile(birthday_reg)

    if not birthday_regex.match(birthday):
        raise ValidationError("생년월일은 YYYYMMDD 형식의 8자리 숫자로 입력해주세요.")
    
def validate_dormitory_code(dormitory_code):
    if Member.objects.filter(Q(username=dormitory_code) & Q(dorm=Dorm.DORM_LIST[0][1])).exists():
        raise ValidationError("이미 가입된 회원이에요!")
    
    dormitory_code_reg = r"^\d{2}-\d{4}$"
    dormitory_code_regex = re.compile(dormitory_code_reg)

    if not dormitory_code_regex.match(dormitory_code):
        raise ValidationError("학사번호는 NN-NNNN 형식으로 입력해주세요. ex)12-3456")
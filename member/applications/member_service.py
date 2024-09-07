from member.domains import MemberRepository
from member.serializers import (
                            SignupRequestSerializer,
                            SignupRequestSerializerV2,
                            SigninRequestSerialzier,
                            SigninResponseSerializer,
                            PasswordChangeRequestSerializer,
                            MemberInfoSerializer,
                        )
from member.domains import Member
from dorm.domains import Dorm
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from utils.exceptions import (
        PasswordWrongError,
        WithdrawedMemberError,
        BannedMemberError,
        SamePasswordError,
    )
from utils.s3 import S3Connect
from django.db import transaction
from datetime import datetime
import pytz

class MemberService:
    def __init__(self, member_repository: MemberRepository):
        self._member_repository = member_repository

    def signup_for_west_dormitory(self, request_data:dict):
        signup_request_serializer = SignupRequestSerializerV2(data=request_data)
        signup_request_serializer.is_valid(raise_exception=True)
        signup_data = signup_request_serializer.validated_data
        member = self._make_member_v2(signup_data)
        self._member_repository.save_member(member)

    """
    deprecated
    """
    def signup(self, request_data: dict):
        signup_request_serializer = SignupRequestSerializer(data=request_data)
        signup_request_serializer.is_valid(raise_exception=True)
        signup_data = signup_request_serializer.validated_data
        url = self._save_dormitory_card_image(signup_data)
        member = self._make_member(signup_data, url)
        self._member_repository.save_member(member)

    def signin(self, request_data: dict):
        signin_request_serializer = SigninRequestSerialzier(data=request_data)
        signin_request_serializer.is_valid(raise_exception=True)
        signin_data: dict = signin_request_serializer.validated_data

        username = signin_data.get('username')
        password = signin_data.get('password')
        member: Member = self._member_repository.find_member_by_username(username=username)

        self._check_login(password, member)

        refresh: RefreshToken = RefreshToken.for_user(member)
        access_token = refresh.access_token

        signin_serializer = SigninResponseSerializer(self.SigninDto(access_token, refresh, member))
        return signin_serializer.data
    
    @transaction.atomic
    def withdraw(self, member: Member):
        anonymizated_member: Member = self._make_member_anonymization(member)
        anonymizated_member.status = 'WITHDRAWAL'
        self._member_repository.save_member(anonymizated_member)

    def change_password(self, request_data, request_user: Member):
        password_change_request_serialzier = PasswordChangeRequestSerializer(data=request_data)
        password_change_request_serialzier.is_valid(raise_exception=True)
        password_data = password_change_request_serialzier.validated_data

        old_password = password_data.get('old_password')
        new_password = password_data.get('new_password')

        self._can_change_password(old_password, new_password, request_user.password)
        request_user.set_password(new_password)
        self._member_repository.save_member(request_user)

    def get_member_info(self, member: Member):
        member_info_serializer = MemberInfoSerializer(member)
        return member_info_serializer.data

    def _save_dormitory_card_image(self, signup_data):
        s3_conn = S3Connect()
        dormitory_card = signup_data.get('dormitory_card')
        name = signup_data.get('name')
        key = s3_conn.make_dormitory_card_s3_key(dormitory_card, name)
        url = s3_conn.upload_to_s3(dormitory_card, key)
        return url

    def _make_member_v2(self, signup_data):
        member = Member(
            password=signup_data.get('birthday'),
            username=signup_data.get('dormitory_code'),
            phone_number=signup_data.get('phone_number'),
            name=signup_data.get('name'),
            birthday=signup_data.get('birthday'),
            dorm=Dorm.objects.get(dorm_name=Dorm.DORM_LIST[2][0]), #서서울관
            status=Member.MEMBER_STATUS_CHOICES[0][0] #PENDING
        )
        return member
    
    """
    deprecated
    """
    def _make_member(self, signup_data, url: str):
        member = Member(
            email=signup_data.get('email'),
            password=self._make_hashed_password(signup_data.get('password')),
            dormitory_code=signup_data.get('dormitory_code'),
            nickname=signup_data.get('nickname'),
            phone_number=signup_data.get('phone_number'),
            name=signup_data.get('name'),
            birthday=signup_data.get('birthday'),
            dormitory_card=url
        )
        return member
    
    def _make_hashed_password(self, password):
        return make_password(password=password)
    
    def _check_login(self, password: str, member: Member):
        if member.status == 'WITHDRAWAL':
            raise WithdrawedMemberError
        
        if len(member.password) <= 8:
            if password != member.password:
                raise PasswordWrongError   
        elif not check_password(password, member.password):
            raise PasswordWrongError
        
        if member.status == 'BANNED':
            raise BannedMemberError

    def _make_member_anonymization(self, target_member: Member) -> Member:
        target_member.set_unusable_password()
        target_member.phone_number = 'unknown'
        target_member.name = 'unknown'
        target_member.birthday = 'unknown'
        return target_member

    def _return_seoul_datetime_object(self):
        seoul_tz = pytz.timezone('Asia/Seoul')
        return datetime.now(seoul_tz)

    def _can_change_password(self, old_password, new_password, request_member_password):
        if len(request_member_password) <= 8:
            if request_member_password != old_password:
                raise PasswordWrongError
        elif not check_password(old_password, request_member_password):
            raise PasswordWrongError
        if check_password(new_password, request_member_password):
            raise SamePasswordError

    class SigninDto:
        def __init__(self, access_token: str, refresh_token: str, member: Member):
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.member = member
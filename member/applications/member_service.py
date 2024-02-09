from member.domains import MemberRepository
from member.serializers import (
                            SignupRequestSerializer,
                            SigninRequestSerialzier,
                            SigninResponseSerializer,
                        )
from member.domains import Member
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from utils.exceptions import PasswordWrongError, WithdrawedMemberError, BannedMemberError, AdminUnAcceptedMemberError
from utils.s3 import S3Connect
from django.contrib.auth.hashers import make_password

class MemberService:
    def __init__(self, member_repository: MemberRepository):
        self._member_repository = member_repository

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

        email = signin_data.get('email')
        password = signin_data.get('password')
        member: Member = self._member_repository.find_member_by_email(email=email)
        self._check_login(password, member)

        refresh: RefreshToken = RefreshToken.for_user(member)
        access_token = refresh.access_token

        signin_serializer = SigninResponseSerializer(self.SigninDto(access_token, refresh, member))
        return signin_serializer.data
    
    def _save_dormitory_card_image(self, signup_data):
        s3_conn = S3Connect()
        dormitory_card = signup_data.get('dormitory_card')
        name = signup_data.get('name')
        key = s3_conn.make_dormitory_card_s3_key(dormitory_card, name)
        url = s3_conn.upload_to_s3(dormitory_card, key)
        return url

    def _make_member(self, signup_data, url: str):
        member = Member(
            email=signup_data.get('email'),
            password=self._make_hashed_password(signup_data.get('password')),
            dormitory_code=signup_data.get('dormitory_code'),
            nickname=signup_data.get('nickname'),
            phone_number=signup_data.get('phone_number'),
            name=signup_data.get('name'),
            dormitory_card=url
        )
        return member
    
    def _make_hashed_password(self, password):
        return make_password(password=password)
    
    def _check_login(self, password: str, member: Member):
        if not check_password(password, member.password):
            raise PasswordWrongError
        if member.status == 'ADMIN_VERIFICATION_PENDING':
            raise AdminUnAcceptedMemberError
        elif member.status == 'WITHDRAWAL':
            raise WithdrawedMemberError
        elif member.status == 'BANNED':
            raise BannedMemberError

    class SigninDto:
        def __init__(self, access_token: str, refresh_token: str, member: Member):
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.member = member
from rest_framework.exceptions import APIException
from rest_framework import status

class PasswordWrongError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '비밀번호가 틀렸습니다. 다시 확인해주세요.'

class RequiredLoginError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '로그인이 필요합니다.'

class WithdrawedMemberError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '이미 탈퇴한 회원입니다.'

class BannedMemberError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '정지된 회원입니다.'

class AdminUnAcceptedMemberError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '아직 학사 정보가 확인되지 않은 회원입니다.'
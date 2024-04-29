from rest_framework import status
from rest_framework.exceptions import APIException

class MessageBlockedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "차단된 이용자입니다."

class MessageToMeError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "자기 자신에게 쪽지를 보낼 수 없습니다."
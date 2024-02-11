from rest_framework.exceptions import APIException
from rest_framework import status

class FCMSendException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'FCM 전송을 실패하였습니다 재시도를 진행합니다.'
from rest_framework.exceptions import APIException
from rest_framework import status

class PostPermissionError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "내가 쓴 글만 수정 및 삭제할 수 있습니다."
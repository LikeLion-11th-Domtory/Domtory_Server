from rest_framework.exceptions import APIException
from rest_framework import status

class PostAuthorExceptionError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "내가 쓴 글은 공감할 수 없습니다."

class PostDuplicateLikeError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "이미 공감한 글입니다."


class CommentAuthorExceptionError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "내가 쓴 댓글은 공감할 수 없습니다."

class CommentDuplicateLikeError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "이미 공감한 댓글입니다."
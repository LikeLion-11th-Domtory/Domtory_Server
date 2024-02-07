from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from member.containers import MembersContainer
from drf_yasg.utils import swagger_auto_schema
from member.serializers import SignupRequestSerializer
from drf_yasg import openapi

response_example = openapi.Response(
    description="An example of a 400 error",
    examples={
        "application/json": {
        "email": ["이미 가입된 회원이에요!"],
        "password": ["영문, 숫자, 특수문자를 조합해 6자 이상, 13자 이하 입력해주세요."],
        "name": ["값을 채워주세요!"],
        "nickname": ["닉네임이 이미 존재해요! 다른 걸로 부탁해요."]
        }
    }
)
class SignUpView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    @swagger_auto_schema(request_body=SignupRequestSerializer, responses={'201': '', '400': response_example})
    def post(self, request):
        """
        회원 가입 API 입니다. form-data로 전송하고 'dormitoryCard'를 포함시켜서 보내주세요.       
        """
        self._members_service.signup(request.data)
        return Response(status=status.HTTP_201_CREATED)
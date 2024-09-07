from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from member.containers import MembersContainer
from drf_yasg.utils import swagger_auto_schema
from member.serializers import SignupRequestSerializerV2
from drf_yasg import openapi

response_example = openapi.Response(
    description="An example of a 400 error",
    examples={
        "application/json": {
        "name": ["값을 채워주세요!"],
        "dormitoryCode" : ["이미 가입된 회원이에요!"]
        }
    }
)
class SignUpView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    @swagger_auto_schema(request_body=SignupRequestSerializerV2, responses={'201': '', '400': response_example})
    def post(self, request):
        """
        회원 가입 API 입니다. form-data로 전송하고 'dormitoryCard'를 포함시켜서 보내주세요.       
        """
        self._members_service.signup_for_west_dormitory(request.data)
        return Response(status=status.HTTP_201_CREATED)
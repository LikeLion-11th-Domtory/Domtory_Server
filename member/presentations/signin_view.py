from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from member.containers import MembersContainer
from drf_yasg.utils import swagger_auto_schema
from member.serializers import SigninRequestSerialzier, SigninResponseSerializer

class SigninView(TokenObtainPairView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    @swagger_auto_schema(request_body=SigninRequestSerialzier, responses={"200": SigninResponseSerializer})
    def post(self, request, *args, **kwargs):
        response = self._members_service.signin(request.data)
        return Response(response, status=status.HTTP_200_OK)

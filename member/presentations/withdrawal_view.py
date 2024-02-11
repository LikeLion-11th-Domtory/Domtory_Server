from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from member.containers import MembersContainer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class WithdrawalView(TokenObtainPairView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    @swagger_auto_schema(responses={"204": ""})
    def post(self, request, *args, **kwargs):
        """"
        회원 탈퇴 API 입니다.
        """
        self._members_service.withdraw(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer
from drf_yasg.utils import swagger_auto_schema
from push.serializers import TokenRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class PushView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._push_service = PushContainer.push_service()

    @swagger_auto_schema(request_body=TokenRequestSerializer, responses={"200": ""})
    def post(self, request):
        """
        FCM 푸시 토큰을 서버로 보내는 API 입니다.
        """
        self._push_service.send_push_token(request.data, request.user)
        return Response(status=status.HTTP_200_OK)
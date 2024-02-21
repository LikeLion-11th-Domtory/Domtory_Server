from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer
from drf_yasg.utils import swagger_auto_schema
from push.serializers import TokenRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class TokenInvalidView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._device_service = PushContainer.device_service()

    @swagger_auto_schema(request_body=TokenRequestSerializer, responses={"204": ""})
    def post(self, request):
        """
        토큰 삭제 API
        """
        self._device_service.delete_device(request.data, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
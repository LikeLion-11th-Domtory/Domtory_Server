from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer
from drf_yasg.utils import swagger_auto_schema
from push.serializers import NotificationDetailResponseSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

authorization_header = openapi.Parameter(
    'Authorization', 
    openapi.IN_HEADER, 
    description="Bearer <token>", 
    type=openapi.TYPE_STRING,
    required=True
)

class NotificationDetailGetView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._notification_detail_service = PushContainer.notification_detail_service()

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200": NotificationDetailResponseSerializer})
    def get(self, request):
        """
        푸시 알람 기록 리스트를 가져오는 api 입니다. 총 20개 불러옵니다.
        """
        response = self._notification_detail_service.get_notification_detail(request.user)
        return Response(response, status=status.HTTP_200_OK)
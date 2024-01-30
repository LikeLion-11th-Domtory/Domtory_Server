from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PushSendView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._push_service = PushContainer.push_service()

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'timezone', 
            in_=openapi.IN_QUERY, 
            description='breakfast, lunch, dinner', 
            type=openapi.TYPE_STRING
        )
        ])
    def post(self, request):
        """
        푸시 알람을 보내는 API 입니다.

        """
        timezone = request.query_params.get("timezone")
        self._push_service.send_push_alarm(timezone)
        return Response(status=status.HTTP_200_OK)
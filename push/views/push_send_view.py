from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer

class PushSendView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._push_service = PushContainer.push_service()

    def post(self, request):
        timezone = request.query_params.get("timezone")
        self._push_service.send_push_alarm(timezone)
        return Response(status=status.HTTP_200_OK)
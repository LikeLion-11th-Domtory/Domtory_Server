from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer

class PushView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._push_service = PushContainer.push_service()

    def post(self, request):
        self._push_service.send_push_token(request.data)
        return Response(status=status.HTTP_200_OK)
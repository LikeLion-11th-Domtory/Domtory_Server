from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from push.containers import PushContainer

class TokenInvalidView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._push_service = PushContainer.push_service()

    def post(self, request):
        """
        삭제 예정 API
        """
        self._push_service.make_token_invalid(request.data)
        return Response(status=status.HTTP_200_OK)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..services import create_message_block

authorization_header = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <token>",
    type=openapi.TYPE_STRING,
    required=True
)

class CreateMessageBlockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":""})
    def post(self, request, target_id):
        response = create_message_block(request, target_id)
        return Response(response, status=status.HTTP_200_OK)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..serializers.message_serializer import MessageRequestSerializer, MessageResponseSerializer, \
    MessageSimpleSerializer
from ..services.message_CRUD import create_message, update_message, delete_messages, get_message_list, \
    get_specific_message_list

authorization_header = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <token>",
    type=openapi.TYPE_STRING,
    required=True
)

class CreateMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], request_body=MessageRequestSerializer, responses={"200":MessageResponseSerializer})
    def post(self, request, target_id):
        response = create_message(request, target_id)
        return Response(response, status = status.HTTP_201_CREATED)

class DeleteMessagesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":""})
    def delete(self, request, target_id):
        response = delete_messages(request, target_id)
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class GetMessageListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":MessageSimpleSerializer})
    def get(self, request):
        response = get_message_list(request)
        return Response(response, status=status.HTTP_200_OK)

class GetSpecificMessageListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":MessageResponseSerializer})
    def get(self, request, target_id):
        response = get_specific_message_list(request, target_id)
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":""})
    def patch(self, request, target_id):
        response = update_message(request, target_id)
        return Response(response, status=status.HTTP_200_OK)
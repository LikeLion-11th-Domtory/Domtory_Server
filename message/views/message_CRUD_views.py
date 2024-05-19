from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..permissions import IsParticipant
from ..services import create_message_room, create_message, delete_messages, read_message, get_message_list, get_specific_message_list
from ..serializers import MessageRoomRequestSerializer, MessageRequestSerializer, MessageResponseSerializer, MessageSimpleSerializer

authorization_header = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <token>",
    type=openapi.TYPE_STRING,
    required=True
)

class CreateMessageRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], request_body=MessageRoomRequestSerializer, responses={"302":"target_id", "201":MessageRequestSerializer})
    def post(self, request, post_id, comment_anonymous_number):
        response = create_message_room(request, post_id, comment_anonymous_number)
        if type(response) is ReturnDict:
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(response, status=status.HTTP_302_FOUND)

class CreateMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[authorization_header], request_body=MessageRequestSerializer, responses={"201":MessageResponseSerializer})
    def post(self, request, message_room_id):
        response = create_message(request, message_room_id)
        return Response(response, status = status.HTTP_201_CREATED)

class DeleteMessagesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipant]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":""})
    def delete(self, request, message_room_id):
        response = delete_messages(request, message_room_id)
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
    permission_classes = [IsParticipant]

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":MessageResponseSerializer})
    def get(self, request, message_room_id):
        response = get_specific_message_list(request, message_room_id)
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200":""})
    def patch(self, request, message_room_id):
        response = read_message(request, message_room_id)
        return Response(response, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from member.containers import MembersContainer
from drf_yasg.utils import swagger_auto_schema
from member.serializers import MemberInfoSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

authorization_header = openapi.Parameter(
    'Authorization', 
    openapi.IN_HEADER, 
    description="Bearer <token>", 
    type=openapi.TYPE_STRING,
    required=True
)

class MemberInfoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    @swagger_auto_schema(manual_parameters=[authorization_header], responses={"200": MemberInfoSerializer})
    def get(self, request):
        """
        유저 정보를 리턴하는 API입니다.
        """
        response = self._members_service.get_member_info(request.user)
        return Response(response, status=status.HTTP_200_OK)
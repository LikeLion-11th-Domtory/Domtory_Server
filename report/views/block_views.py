from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from board.models import *
from report.serializers.block_serializer import *
from report.serializers.report_serializer import *
from report.services.block_board import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from board.permissions import IsStaffOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from report.services.create_report import *
# Create your views here.


class blockPostOrCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    @swagger_auto_schema(request_body=IsBlindRequestSerializer, responses={"200": ""})
    def post(self, request):
        """
        특정 게시글/게시판을 block 시키는 view 입니다.
        type에는 종류에 따라서 'post' 아니면 'comment'가 들어갑니다.
        """

        block_board(request)

        return Response(status=status.HTTP_200_OK)
    


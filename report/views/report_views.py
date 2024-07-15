from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from board.models import *
from report.serializers.block_serializer import *
from report.serializers.report_serializer import *
from report.services.block_board import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from board.permissions import IsStaffOrReadOnly
from board.models import Post, Comment
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from report.services.create_report import *
# Create your views here.

class CreateReportView(APIView):
    # authentication_classes = [JWTAuthentication]

    def post(self, request, target_type, target_id):
        response = create_report(request, target_type, target_id)

        return Response(response, status=status.HTTP_201_CREATED)
    
        


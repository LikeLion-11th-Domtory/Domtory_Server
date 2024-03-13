from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsStaffOrReadOnly
from ..services import create_post

class CouncilPostCreateView(APIView):
    """
    자율회 게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def post(self, request):
        response = create_post(request, 6)
        return Response(response, status = status.HTTP_201_CREATED)
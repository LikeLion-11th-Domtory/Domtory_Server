from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsStaffOrReadOnly

from board.models.board_models import Board
from board.services.popular_board_list import get_popular_board_list


class PopularBoardListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        response = get_popular_board_list(request)
        return Response(response, status=status.HTTP_200_OK)





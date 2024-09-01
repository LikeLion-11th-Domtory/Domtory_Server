from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from ..permissions import IsStaffOrReadOnly
from board.services.popular_board_list import *


class PopularBoardListViewV2(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        response = find_popular_post_by_dorm_id(request)
        return Response(response, status=status.HTTP_200_OK)


class PopularBoardListView(APIView):
    """
    deprecated
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        response = get_popular_board_list(request)
        return Response(response, status=status.HTTP_200_OK)





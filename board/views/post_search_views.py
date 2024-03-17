from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..services import (search_post_in_board,
                        search_post_in_all_boards,
                        paginate_and_search_post_in_board)


class PostSearchView(APIView):
    """
    게시글 검색 뷰 (페이지네이션으로 대체 예정)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, board_id):
        word_list = request.data['word_list']
        if board_id != 0: # 하나의 게시판에 대하여 검색
            result = search_post_in_board(word_list, board_id)
        else: # 모든 게시판에 대하여 검색
            result = search_post_in_all_boards(word_list)
        return Response(result, status = status.HTTP_200_OK)
    

class PaginatedPostSearchView(APIView):
    """
    게시글 검색 결과를 페이지네이션하여 반환하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        word_list = request.data['word_list']
        result = paginate_and_search_post_in_board(request, word_list, board_id)
        return Response(result, status = status.HTTP_200_OK)
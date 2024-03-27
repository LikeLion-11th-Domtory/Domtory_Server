from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from board.services.bookmark import bookmark_post, bookmark_post_list

class BookmarkPostView(APIView):
    """
    스크랩 등록/취소 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        response = bookmark_post(request, post_id)
        return Response(response, status = status.HTTP_200_OK)
    

class BookmarkListView(APIView):
    """
    스크랩한 게시글 리스트 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = bookmark_post_list(request)
        return Response(response, status = status.HTTP_200_OK)
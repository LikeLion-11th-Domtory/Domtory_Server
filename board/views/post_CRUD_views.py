from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..permissions import IsStaffOrReadOnly
from ..services.post_CRUD import *


class PostCreateViewV2(APIView):
    """
    게시글 작성 뷰(확장 이후)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        response = create_post_v2(request, board_id)
        return Response(response, status = status.HTTP_201_CREATED)



class PostCreateView(APIView):
    """
    deprecated
    게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):
        response = create_post(request, board_id)
        return Response(response, status = status.HTTP_201_CREATED)


class PostUpdateView(APIView):
    """
    게시글 수정 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_id):
        response = update_post(request, post_id)
        return Response(response, status = status.HTTP_200_OK)


class PostDeleteView(APIView):
    """
    게시글 삭제 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        response = delete_post(request, post_id)
        return Response(response, status = status.HTTP_204_NO_CONTENT)


class PostDetailView(APIView):
    """
    게시글 디테일 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        response = get_post_detail(request, post_id)
        return Response(response, status = status.HTTP_200_OK)
    

class CouncilPostCreateView(APIView):
    """
    자율회 게시글 작성 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaffOrReadOnly]

    def post(self, request):
        response = create_post(request, 6)
        return Response(response, status = status.HTTP_201_CREATED)
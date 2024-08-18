from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from ..services import *

class PostListView(APIView):
    """
    deprecated
    게시판별 리스트 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        result = unpaginated_post_list(request, board_id)
        return Response(result, status = status.HTTP_200_OK)


class PaginatedPostListView(APIView):
    """
    deprecated
    게시판별 리스트를 페이지네이션하여 반환
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        result = paginated_post_list(request, board_id)
        return Response(result, status = status.HTTP_200_OK)


class FreeBoardSimpleView(APIView):
    """
    deprecated
    특정/전체 게시판의 최근 게시물을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        if board_id != 0: # 특정 게시판에 대하여
            result = recent_posts_in_board(board_id)
        else: # 전체 게시판에 대하여
            result = recent_posts_in_all_boards()
        return Response(result, status = status.HTTP_200_OK)
    

class MyPostView(APIView):
    """
    마이페이지에서 내가 쓴 게시글을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = my_posts(request.user)
        return Response(result, status = status.HTTP_200_OK)
    

class MyCommentView(APIView):
    """
    내가 댓글을 쓴 게시글들을 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = my_comments(request.user)
        return Response(result, status = status.HTTP_200_OK)
    

class PaginatedMyPostView(APIView):
    """
    내가 쓴 게시글을 페이지네이션하여 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = paginated_my_posts_list(request, request.user)
        return Response(result, status = status.HTTP_200_OK)
    

class PaginatedMyCommentView(APIView):
    """
    내가 댓글을 쓴 게시글을 페이지네이션하여 출력하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = paginated_my_comments(request, request.user)
        return Response(result, status = status.HTTP_200_OK)


class PostListByDormView(APIView):
    """
    유저의 기숙사에 맞는 게시판을 조회하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        result = get_posts_by_dorm(request, board_id)
        return Response(result, status = status.HTTP_200_OK)


class RecentPostListView(APIView):
    """
    자신이 속한 기숙사의 자유게시판 최신 게시글 5개를 조회하는 뷰
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        result = get_recent_posts_by_dorm(request, board_id)
        return Response(result, status = status.HTTP_200_OK)




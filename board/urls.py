from django.urls import path
from .views import *
from .views.popular_board_list_views import *
from .views.like_views import *

app_name = 'board'

urlpatterns = [
    # 게시글 API
    path('post/create/<int:board_id>/', PostCreateView.as_view()), # 게시글 생성
    path('post/detail/<int:post_id>/', PostDetailView.as_view()), # 게시글 상세정보
    path('post/update/<int:post_id>/', PostUpdateView.as_view()), # 게시글 수정
    path('post/delete/<int:post_id>/', PostDeleteView.as_view()), # 게시글 삭제
    path('post/list/<int:board_id>/', PostListView.as_view()), # 특정 게시판의 게시글 리스트
    path('post/latest/<int:board_id>/', FreeBoardSimpleView.as_view()), # 특정 게시판의 최근 5개 게시글
    path('post/search/<int:board_id>/', PostSearchView.as_view()), # 게시글 검색
    path('post/create/council/', CouncilPostCreateView.as_view()), # 자율회 게시글 생성

    # 댓글 API
    path('comment/create/<int:post_id>/', CommentCreateView.as_view()), # 댓글 작성
    path('comment/delete/<int:comment_id>/', CommentDeleteView.as_view()), # 댓글 삭제
    path('reply/create/<int:comment_id>/', ReplyCreateView.as_view()), #대댓글 작성
    path('reply/delete/<int:reply_id>/', ReplyDeleteView.as_view()), # 대댓글 삭제

    # 마이페이지
    path('mypage/post/', MyPostView.as_view()), # 내가 쓴 게시글
    path('mypage/comment/', MyCommentView.as_view()), # 내가 댓글을 쓴 게시글

    # 페이지네이션 추가 API
    path('post/paged/list/<int:board_id>/', PaginatedPostListView.as_view()), # 특정 게시판의 게시글 리스트
    path('mypage/paged/post/', PaginatedMyPostView.as_view()), # 내가 쓴 게시글
    path('mypage/paged/comment/', PaginatedMyCommentView.as_view()), # 내가 댓글을 쓴 게시글
    path('post/paged/search/<int:board_id>/', PaginatedPostSearchView.as_view()), # 검색 결과를 페이지네이션하여 반환

    # 좋아요, 핫게 관련 API
    path('post/paged/list/popular/', PopularBoardListView.as_view()), #핫게시판 게시글 리스트 (페이지네이션)
    path('post/like/<int:post_id>/', PostLikeView.as_view()), #게시물 좋아요
    path('comment/like/<int:comment_id>/', CommentLikeView.as_view()), #댓글 좋아요

    # 스크랩 API
    path('post/bookmark/<int:post_id>/', BookmarkPostView.as_view()), # 게시글을 스크랩
    
]
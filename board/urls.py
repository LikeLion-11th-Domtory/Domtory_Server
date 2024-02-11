from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    # 게시글 API
    path('post/create/<int:board_id>/', PostCreateView.as_view()),
    path('post/detail/<int:post_id>/', PostDetailView.as_view()),
    path('post/update/<int:post_id>/', PostUpdateDeleteView.as_view()),
    path('post/list/<int:board_id>/', PostListView.as_view()),
    path('post/latest/freeboard/', FreeBoardSimpleView.as_view()),

    # 이미지 API
    # path('image/upload/<int:post_id>/', ImageUploadView.as_view()),
    # path('image/delete/<int:image_id>/', ImageDeleteView.as_view()),

    # 댓글 API
    path('comment/create/<int:post_id>/', CommentCreateView.as_view()),
    path('comment/delete/<int:comment_id>/', CommentDeleteView.as_view()),
    path('reply/create/<int:comment_id>/', ReplyCreateView.as_view()),
    path('reply/delete/<int:reply_id>/', ReplyDeleteView.as_view()),
]
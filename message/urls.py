from django.urls import path

from .views.message_CRUD_views import *
from .views.message_block_views import CreateMessageBlockView

app_name = 'message'

urlpatterns = [
    path('send/inpost/<int:post_id>/<int:comment_anonymous_number>/', CreateMessageRoomView.as_view()),
    path('send/inroom/<int:message_room_id>/', CreateMessageView.as_view()),
    path('list/', GetMessageListView.as_view()),
    path('delete/<int:message_room_id>/', DeleteMessagesView.as_view()),
    path('detail/<int:message_room_id>/', GetSpecificMessageListView.as_view()),
    path('block/<int:target_id>/', CreateMessageBlockView.as_view()),
]
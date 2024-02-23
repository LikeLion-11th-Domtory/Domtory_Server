from django.urls import path
from push.views import (
    PushView,
    PushSendView, 
    TokenInvalidView,
    PushListGetVIew,
    PushCheckView,
    PushDeleteView,
)

app_name = 'push'

urlpatterns = [
    path('token/', PushView.as_view()),
    path('send/', PushSendView.as_view()),
    path('token/invalid/', TokenInvalidView.as_view()),
    path('list/', PushListGetVIew.as_view()),
    path('check/', PushCheckView.as_view()),
    path('delete/', PushDeleteView.as_view()),
]
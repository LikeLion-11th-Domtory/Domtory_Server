from django.urls import path
from push.views import PushView, PushSendView, TokenInvalidView

app_name = 'push'

urlpatterns = [
    path('token/', PushView.as_view()),
    path('send/', PushSendView.as_view()),
    path('token/invalid/', TokenInvalidView.as_view())
]
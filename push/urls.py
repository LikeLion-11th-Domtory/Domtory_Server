from django.urls import path
from push.views import PushView, PushSendView

app_name = 'push'

urlpatterns = [
    path('token/', PushView.as_view()),
    path('send/', PushSendView.as_view()),
]
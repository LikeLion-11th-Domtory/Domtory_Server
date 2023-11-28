from django.urls import path
from push.views import PushView

app_name = 'push'

urlpatterns = [
    path('token/', PushView.as_view())
]
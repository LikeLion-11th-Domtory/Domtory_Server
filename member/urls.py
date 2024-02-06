from django.urls import path
from member.presentations import (
                                    SignUpView,
                                    SigninView,
                                )

app_name = 'member'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
]
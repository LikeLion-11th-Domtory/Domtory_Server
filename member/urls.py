from django.urls import path
from member.presentations import (
                                    SignUpView,
                                    SigninView,
                                    WithdrawalView,
                                    PasswordChangeView,
                                    MemberInfoView,
                                )

app_name = 'member'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('info/', MemberInfoView.as_view(), name='member_info'),
]
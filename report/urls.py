from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('<str:target_type>/<int:target_id>/', CreateReportView.as_view()),
    # path('<str:target_type>/<int:target_id>/get/', ReadReportView.as_view()),
]
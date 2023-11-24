from django.urls import path
from .views import *

app_name = 'notice'

urlpatterns = [
    path('notice/', NoticeListView.as_view(), name='notice_list'),
    path('<int:id>/', NoticeDetailView.as_view(), name='notice_detail'),
]
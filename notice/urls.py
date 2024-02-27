from django.urls import path
from .views import *
from .parser_view import *

app_name = 'notice'

urlpatterns = [
    path('crawling/all/', CrawlAllNoticeView.as_view(), name='parser_view'),
    path('crawling/daily/', CrawlNoticeDailyView.as_view(), name='parser_view'),
    path('', NoticeListView.as_view(), name='notice_list'),
    path('<int:id>/', NoticeDetailView.as_view(), name='notice_detail'),
]
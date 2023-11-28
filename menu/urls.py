from django.urls import path
from .views import *
from .crawling_view import CrawlingView

app_name = 'menu'

urlpatterns = [
    path('<str:date_code>/<str:option>/', MenuListView.as_view(), name='menu_list'),
    path('crawling/', CrawlingView.as_view(), name='crawling')
]
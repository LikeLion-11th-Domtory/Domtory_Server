from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    path('<str:date_code>/<str:option>/', MenuListView.as_view(), name='menu_list'),
]
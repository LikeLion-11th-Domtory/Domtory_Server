from django.urls import path
from .views import *

app_name = 'menu'

urlpatterns = [
    
    path('list/<str:date_code>/', MenuListView.as_view(), name='menu_list'),
    path('breakfast/<str:date_code>/', BreakfastView.as_view(), name='breakfast'),
    path('lunch/<str:date_code>/', LunchView.as_view(), name='lunch'),
    path('dinner/<str:date_code>/', DinnerView.as_view(), name='dinner'),
    
]
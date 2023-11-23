from .models import Menu
from .serializers import MenuSerializer, BreakfastSerializer, LunchSerializer, DinnerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# 날짜에 맞는 전체 식단 조회
class MenuListView(APIView):
    def get(self, request, date_code):
        menus = Menu.objects.filter(date_code=date_code)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 날짜에 맞는 아침 식단 조회
class BreakfastView(APIView):
    def get(self, request, date_code):
        menus = Menu.objects.filter(date_code=date_code)
        serializer = BreakfastSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 날짜에 맞는 점심 식단 조회
class LunchView(APIView):
    def get(self, request, date_code):
        menus = Menu.objects.filter(date_code=date_code)
        serializer = LunchSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 날짜에 맞는 저녁 식단 조회
class DinnerView(APIView):
    def get(self, request, date_code):
        menus = Menu.objects.filter(date_code=date_code)
        serializer = DinnerSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

import datetime

from .models import Menu
from .serializers import MenuListSerializer, BreakfastListSerializer, LunchListSerializer, DinnerListSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


def find_sunday(date_code):
    date = datetime.datetime.strptime(date_code, '%y%m%d').date()
    days_to_subtract = (date.weekday() + 1) % 7
    sunday = date - datetime.timedelta(days=days_to_subtract)
    return sunday.strftime('%y%m%d')


# 날짜에 맞는 식단 조회: total이면 전부 조회, 아니면 아침, 점심, 저녁 중 하나만 조회
class MenuListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, date_code, option):
        if option == 'total':
            sunday = find_sunday(date_code)
            saturday = (datetime.datetime.strptime(sunday, '%y%m%d').date() + datetime.timedelta(days=6)).strftime('%y%m%d')
            menus = Menu.objects.filter(date_code__gte=sunday, date_code__lte=saturday, dorm = request.user.dorm)
            serializer = MenuListSerializer(menus, many=True, context = {'request' : request})
        else:
            menus = Menu.objects.filter(date_code=date_code, dorm = request.user.dorm)
            if option == 'breakfast':
                serializer = BreakfastListSerializer(menus, many=True, context = {'request' : request})
            elif option == 'lunch':
                serializer = LunchListSerializer(menus, many=True, context = {'request' : request})
            elif option == 'dinner':
                serializer = DinnerListSerializer(menus, many=True, context = {'request' : request})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

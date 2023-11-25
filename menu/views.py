from .models import Menu
from .serializers import MenuSerializer, BreakfastSerializer, LunchSerializer, DinnerSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# 날짜에 맞는 식단 조회: total이면 전부 조회, 아니면 아침, 점심, 저녁 중 하나만 조회
class MenuListView(APIView):
    def get(self, request, date_code, option):
        menus = Menu.objects.filter(date_code=date_code)
        if option == 'total':
            serializer = MenuSerializer(menus, many=True)
        elif option == 'breakfast':
            serializer = BreakfastSerializer(menus, many=True)
        elif option == 'lunch':
            serializer = LunchSerializer(menus, many=True)
        elif option == 'dinner':
            serializer = DinnerSerializer(menus, many=True)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

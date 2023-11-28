# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from .serializers import MenuSerializer, BreakfastListSerializer, LunchListSerializer, DinnerListSerializer
import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from .models import Breakfast, Lunch, Dinner, Menu
from django.shortcuts import get_object_or_404
class CrawlingView(APIView):
    def post(self, request):
        url = 'http://cbhs2.kr/meal?searchWeek=0'
        
        # 웹페이지에서 HTML 내용을 가져온다
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text
        
        # BeautifulSoup 객체를 생성하여 HTML을 파싱.
        soup = BeautifulSoup(html, 'html.parser')
        
        # 모든 식단 찾기
        meal_plans = soup.find_all('div', class_='fplan_plan')

        # 각 식단 계획에 대해 요일과 식사 시간대별 메뉴 추출
        for plan in meal_plans:
            try:
                # 날짜 정보
                date_detail = plan.find('a', class_='btn_type1 fplan_date_sun').text.strip()
                date_code = date_detail[:8].replace('.', '')

                # 해당 일의 식단 정보를 저장할 딕셔너리 생성
                meal_info = {
                    'breakfast': '',
                    'lunch': '',
                    'dinner': ''
                }
                # 조식, 중식, 석식 메뉴 추출
                meals = plan.find_all(['h3', 'p'], recursive=False)
                current_meal = None
                for item in meals:
                    if item.name == 'h3':
                        if '조식' in item.text:
                            current_meal = 'breakfast'
                        elif '중식' in item.text:
                            current_meal = 'lunch'
                        elif '석식' in item.text:
                            current_meal = 'dinner'
                    elif item.name == 'p' and current_meal:
                        meal_info[current_meal] = item.text.strip()

                # 식단 date 저장
                menu_serializer = MenuSerializer(data={'date_code': date_code, 'date_detail': date_detail})
                menu_serializer.is_valid(raise_exception=True)
                menu = menu_serializer.save()
                
                breakfast_data = meal_info.pop('breakfast').split(',')
                lunch_data = meal_info.pop('lunch').split(',')
                dinner_data = meal_info.pop('dinner').split(',')
                
                for breakfast in breakfast_data:
                    breakfast = Breakfast(menu=menu, name=breakfast)
                    breakfast.save()
                
                for lunch in lunch_data:
                    lunch = Lunch(menu=menu, name=lunch)
                    lunch.save()
                
                for dinner in dinner_data:
                    dinner = Dinner(menu=menu, name=dinner)
                    dinner.save()

            except:
                pass
        return Response(status=status.HTTP_200_OK)
        

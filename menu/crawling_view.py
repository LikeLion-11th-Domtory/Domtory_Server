# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from .serializers import MenuSerializer
import requests
from bs4 import BeautifulSoup

def crawling():
    url = 'http://cbhs2.kr/meal?searchWeek=0'

    # 웹페이지에서 HTML 내용을 가져온다
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text

    # BeautifulSoup 객체를 생성하여 HTML을 파싱.
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 식단 찾기
    meal_plans = soup.find_all('div', class_='fplan_plan')

    try:
        # 각 식단 계획에 대해 요일과 식사 시간대별 메뉴 추출
        for plan in meal_plans:
            # 날짜 정보
            date_detail = plan.find('a', class_='btn_type1 fplan_date_sun').text.strip()
            date_code = date_detail[:8].replace('.', '')
            # 해당 일의 식단 정보를 저장할 딕셔너리 생성
            meal_info = {
                'date_detail': date_detail,
                'date_code': date_code,
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
            
            print(meal_info)
            
            # 식단 정보 저장
            menu = MenuSerializer(data=meal_info)
            if menu.is_valid():
                menu.save()
            else:
                return Response(menu.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        pass

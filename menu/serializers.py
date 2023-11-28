from django.core import serializers
from rest_framework import serializers
from .models import Menu, Breakfast, Lunch, Dinner

class BreakfastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['breakfast']


class BreakfastListSerializer(serializers.ModelSerializer):
    breakfast_list = BreakfastSerializer(many=True, read_only=True, source='breakfast_set')
    class Meta:
        model = Menu
        fields = ['breakfast_list']


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['lunch']


class LunchListSerializer(serializers.ModelSerializer):
    lunch_list = LunchSerializer(many=True, read_only=True, source='lunch_set')
    class Meta:
        model = Menu
        fields = ['lunch_list']


class DinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['dinner']


class DinnerListSerializer(serializers.ModelSerializer):
    dinner_list = DinnerSerializer(many=True, read_only=True, source='dinner_set')
    class Meta:
        model = Menu
        fields = ['dinner_list']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_code', 'date_detail']


class MenuListSerializer(serializers.ModelSerializer):
    breakfast_list = BreakfastSerializer(many=True, read_only=True, source='breakfast_set')
    lunch_list = LunchSerializer(many=True, read_only=True, source='lunch_set')
    dinner_list = DinnerSerializer(many=True, read_only=True, source='dinner_set')
    class Meta:
        model = Menu
        fields = ['date_code', 'date_detail', 'breakfast_list', 'lunch_list', 'dinner_list']
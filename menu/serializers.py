from django.core import serializers
from rest_framework import serializers
from .models import Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_code', 'date_detail', 'breakfast', 'lunch', 'dinner']


class BreakfastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_detail', 'breakfast']


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_detail', 'lunch']


class DinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_detail', 'dinner']

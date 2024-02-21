from django.core import serializers

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from .models import Menu


class BreakfastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['breakfast']


class BreakfastListSerializer(serializers.ModelSerializer):
    breakfast_list = BreakfastSerializer(many=True, read_only=True, source='breakfast_set')

    class Meta:
        model = Menu
        fields = ['breakfast_list']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['breakfast_list'] = [breakfast_list.name for breakfast_list in instance.breakfast.all()]
        return ret


class LunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['lunch']


class LunchListSerializer(serializers.ModelSerializer):
    lunch_list = LunchSerializer(many=True, read_only=True, source='lunch_set')

    class Meta:
        model = Menu
        fields = ['lunch_list']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['lunch_list'] = [lunch_list.name for lunch_list in instance.lunch.all()]
        return ret


class DinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['dinner']


class DinnerListSerializer(serializers.ModelSerializer):
    dinner_list = DinnerSerializer(many=True, read_only=True, source='dinner_set')

    class Meta:
        model = Menu
        fields = ['dinner_list']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['dinner_list'] = [dinner_list.name for dinner_list in instance.dinner.all()]
        return ret


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['date_code', 'date_detail']


class MenuListSerializer(serializers.ModelSerializer):
    breakfast_list = BreakfastSerializer(read_only=True, source='breakfast_set')
    lunch_list = LunchSerializer(read_only=True, source='lunch_set')
    dinner_list = DinnerSerializer(read_only=True, source='dinner_set')

    class Meta:
        model = Menu
        fields = ['date_code', 'date_detail', 'breakfast_list', 'lunch_list', 'dinner_list']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['breakfast_list'] = [breakfast_list.name for breakfast_list in instance.breakfast.all()]
        ret['lunch_list'] = [lunch_list.name for lunch_list in instance.lunch.all()]
        ret['dinner_list'] = [dinner_list.name for dinner_list in instance.dinner.all()]
        return ret

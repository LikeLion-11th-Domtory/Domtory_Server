from rest_framework import serializers
from ..domains import Dorm

class DormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dorm
        fields = ['id', 'dorm_name']


class DormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dorm
        fields = '__all__'
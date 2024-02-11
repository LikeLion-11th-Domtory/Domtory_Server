from rest_framework import serializers
from ..models import Board
from .post_serializer import *

class BoardRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name' 'description']


class BoardResponseSerializer(serializers.ModelSerializer):
    post = PostResponseSerializer(many = True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'post']
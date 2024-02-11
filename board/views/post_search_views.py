from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..serializers import *
from ..models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *
from django.db.models import Q


class PostSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        word_list = request.data['word_list']
        query = Q()
        for keyword in word_list:
            query |= Q(body__icontains=keyword) | Q(title__icontains=keyword)
        
        posts = Post.objects.filter(query)
        return Response(PostResponseSerializer(posts, many = True).data)
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
    
    def post(self, request, board_id):
        word_list = request.data['word_list'].split()
        query = Q()

        for keyword in word_list: # Q 객체에 검색어 추가
            query |= Q(body__search=keyword) | Q(title__search=keyword)

        if board_id != 0: # 특정 게시판에 대하여 검색 시
            posts = Post.objects.filter(Q(board = board_id) & query).order_by('-created_at')
        else: # 전체 게시판에 대하여 검색 시
            posts = Post.objects.filter(query).order_by('-created_at')
        return Response(PostSimpleSerializer(posts, many = True).data, status = status.HTTP_200_OK)
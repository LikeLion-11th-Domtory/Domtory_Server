from django.shortcuts import render
from .models import NoticeList
from .serializers import NoticeListSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import *

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


# Create your views here.

#페이지네이션
class PostPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            ('postList', data),
        ]))
    
class NoticeListView(generics.ListAPIView):
    queryset = NoticeList.objects.all().order_by('-date')
    serializer_class = NoticeListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #페이지네이션
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        queryset = NoticeList.objects.filter(dorm = self.request.user.dorm)
        return queryset

class NoticeDetailView(generics.RetrieveAPIView):
    queryset = NoticeList.objects.all()
    serializer_class = NoticeListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

# class NoticeSearchView(generics.ListAPIView):
#     serializer_class = NoticeListSerializer
    
#     def get_queryset(self):
#         queryset = NoticeList.objects.all()
#         title = self.request.query_params.get('title', None)
        
#         if title is not None:
#             queryset = queryset.filter(title__icontains=title)
#         return queryset


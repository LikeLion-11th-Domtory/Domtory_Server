from django.shortcuts import render
from .models import NoticeList
from .serializers import NoticeListSerializer
from rest_framework import generics

# Create your views here.

class NoticeListView(generics.ListAPIView):
    queryset = NoticeList.objects.all()
    serializer_class = NoticeListSerializer

class NoticeDetailView(generics.RetrieveAPIView):
    queryset = NoticeList.objects.all()
    serializer_class = NoticeListSerializer
    lookup_field = 'id'

# class NoticeSearchView(generics.ListAPIView):
#     serializer_class = NoticeListSerializer
    
#     def get_queryset(self):
#         queryset = NoticeList.objects.all()
#         title = self.request.query_params.get('title', None)
        
#         if title is not None:
#             queryset = queryset.filter(title__icontains=title)
#         return queryset


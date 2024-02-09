from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# from board.models import *
from .serializers import *

# Create your views here.

class CreateReportView(APIView):
    # response = requests.post('', params=)
    def post(self, request, target_id, target_type):
        if target_type == "post":
            target = Post.objects.get(pk=target_id)
            data = request.data.copy()
            data['post_id'] = target_id

        elif target_type == "comment":
            target = Comment.objects.get(pk=target_id)
            data = request.data.copy()
            data['comment_id'] = target.id
        
        serializer = ReportSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # 람다 서버에 보내서 욕설 체크
            dataset = {"target":target.request_body, 'targetId':target.id, 'reportId':data[id]}
            response = requests.post('', params=dataset)
            # if response['statusCode'] == 200:

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UpdateReportStatusView(APIView):
    #PENDING일 경우
    def put(self, request, target_id, target_type):
        if target_type == "post":
            target = Post.objects.get(pk=target_id)
        elif target_type == "comment":
            target = Comment.objects.get(pk=target_id)

        serializer = UpdateReportSerializer(target, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def check_reports():
#     dataset = {"target":target.request_body, 'targetId':target.id, 'reportId':data[id]}
#     response = requests.post('', params=)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from board.models import *
from .serializers import *

import json

# Create your views here.

class CreateReportView(APIView):
    def post(self, request, target_type, target_id):
        if target_type == "post":
            target = Post.objects.get(pk=target_id)
            data = request.data.copy()
            data['post'] = target_id

        elif target_type == "comment":
            target = Comment.objects.get(pk=target_id)
            data = request.data.copy()
            data['comment'] = target_id
        
        serializer = ReportSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # 람다 서버에 보내서 욕설 체크
            dataset = {
                "target" : target.body,
                'target_id' : target.id,
                'table' : target_type,
                'report_id' : serializer.data['id']
            }
            # dataset = json.dumps(dataset, ensure_ascii=False)
            response = requests.post('https://8ufbqa4zl8.execute-api.ap-northeast-2.amazonaws.com/prod', json=dataset)
            print(response.content)
            print(dataset)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


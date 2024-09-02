import requests
from rest_framework.response import Response
from report.models.report_models import *
from report.serializers.report_serializer import *


def create_report(request, target_type, target_id):
    if target_type == "post":
        target = Post.objects.get(pk=target_id)
        serializer = ReportPostSerializer(data={'post': target.id, 'dorm': target.dorm.id})

    elif target_type == "comment":
        target = Comment.objects.get(pk=target_id)
        serializer = ReportCommentSerializer(data={'comment': target.id, 'dorm': target.dorm.id})

    elif target_type == "message":
        target = Message.objects.get(pk=target_id)
        serializer = ReportMessageSerializer(data={'message': target.id, 'dorm': target.sender.dorm.id})
    
     # post, comment, message 외래키 연결해서 역직렬화
    
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # 람다 서버에 보내서 욕설 체크
    dataset = {
        "target" : target.body,
        'target_id' : target.id,
        'table' : target_type,
        'report_id' : serializer.data['id']
    }
    requests.post('https://8ufbqa4zl8.execute-api.ap-northeast-2.amazonaws.com/prod', json=dataset)

    return serializer.data
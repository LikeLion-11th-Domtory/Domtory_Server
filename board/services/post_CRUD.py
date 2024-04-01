from ..serializers import PostRequestSerializer, PostResponseSerializer, ImageRequestSerializer, CommentResponseSerializer
from ..models import Board, PostImage, Post, Comment
from utils.s3 import S3Connect
from push.tasks import send_push_notification_handler
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

"""
게시글 디테일 페이지
"""
def get_post_detail(request, post_id):
    reply_prefetch = Prefetch(
        'reply',
        queryset=Comment.objects.all().order_by('created_at')
    )
    comment_prefetch = Prefetch(
        'comment',
        queryset=Comment.objects.prefetch_related(reply_prefetch).filter(parent = None).order_by('created_at')
    )
    post = get_object_or_404(
        Post.objects.prefetch_related(comment_prefetch),
        id = post_id
    )
    response = PostResponseSerializer(post, context = {'request' : request}).data
    return response


"""
게시글 작성 메소드
"""
def create_post(request, board_id):
    board = Board.objects.get(pk = board_id)
    serializer = PostRequestSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    post = serializer.save(member = request.user, board = board)

    if post.board_id == 4:
        send_push_notification_handler.delay('post-notification-event', post_id=post.id)
    elif post.board_id == 6:
        send_push_notification_handler.delay('post-notification-event', post_id=post.id)

    if 'images' not in request.data:
        response = get_post_detail(request, post.id)
        return response

    image_request_serializer = ImageRequestSerializer(data = request.data)
    image_request_serializer.is_valid(raise_exception=True)
    image_data = image_request_serializer.validated_data
    image_list = image_data.get('images')

    if image_list:
        s3 = S3Connect()
        s3.upload_resized_image(post, image_list)
    
    response = get_post_detail(request, post.id)
    return response


"""
게시글 수정
"""
def update_post(request, post):
    if 'title' in request.data:
        post.title = request.data['title']

    if 'body' in request.data:
        post.body = request.data['body']
        
    if 'deleted_images' in request.data:
        deleted_images = request.data.getlist('deleted_images')
        PostImage.objects.filter(id__in=map(int, deleted_images)).delete()

    if 'images' in request.data:
        image_serializer = ImageRequestSerializer(data = request.data)
        image_serializer.is_valid(raise_exception = True)
        image_data = image_serializer.validated_data
        image_list = image_data.get('images')
        if image_list:
            s3 = S3Connect()
            s3.upload_resized_image(post, image_list)
            first_image = post.post_image.first()
            if first_image:
                post.thumbnail_url = first_image.image_url
            else:
                post.thumbnail_url = None
            post.save()
    first_image = post.post_image.first()

    if first_image:
        post.thumbnail_url = first_image.image_url
    else:
        post.thumbnail_url = None
    post.save()
    response = get_post_detail(request, post.id)
    return response


"""
게시글 삭제
"""
def delete_post(post):
    post.is_deleted = True
    post.save()
    res = {
        "msg" : "게시글 삭제 완료"
    }
    return res
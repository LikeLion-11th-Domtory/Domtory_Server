from decouple import config
import boto3
from PIL import Image, ImageOps
from io import BytesIO
import uuid
from board.models import PostImage, Post

class S3Connect:
    _aws_access_key = config('AWS_ACCESS_KEY')
    _aws_secret_key = config('AWS_SECRET_ACCESS_KEY')
    _bucket_name = config('BUCKET_NAME')
    
    def __init__(self):
        self._s3_conn = boto3.client('s3', aws_access_key_id=self._aws_access_key, aws_secret_access_key=self._aws_secret_key)

    def make_dormitory_card_s3_key(self, image_data, name):
        object_name = f"{name}.{image_data.content_type.split('/')[-1]}"
        return '학사카드/' + object_name
    
    def upload_to_s3(self, image_data, key, content_type=None):
        if content_type:
            self._s3_conn.put_object(Body=image_data, Bucket=self._bucket_name, Key=key, ContentType=content_type)
        else:
            self._s3_conn.put_object(Body=image_data, Bucket=self._bucket_name, Key=key, ContentType=image_data.content_type)
        url = f"https://{self._bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}"
        return url

    def delete_object(self, key: str):
        self._s3_conn.delete_object(Bucket=self._bucket_name, Key=key)

    def upload_resized_image(self, post, image_list):
        s3 = S3Connect()
        for i in range(0, len(image_list)):
            image = Image.open(image_list[i])
            image = ImageOps.exif_transpose(image)
            image = image.convert('RGB')

            image.thumbnail((2000, 2000))
            buffer = BytesIO()
            image.save(buffer, format = 'JPEG', quality = 80)
            image_data = buffer.getvalue()

            key = f"{post.board.name}/{post.pk}_{uuid.uuid4().hex}.jpeg"
            image_url = s3.upload_to_s3(image_data = image_data, key = key, content_type = 'image/jpeg')
            
            PostImage(post = post, image_url = image_url).save()
            
            if i == 0:
                post.thumbnail_url = image_url
                post.save()
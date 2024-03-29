from decouple import config
import boto3

def get_dynamodb_table(table_name):
    AWS_ACCESS_KEY=config('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY')
    
    dynamodb = boto3.resource(
        'dynamodb', region_name='ap-northeast-2',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return dynamodb.Table(table_name)
    
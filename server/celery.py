import os
from celery import Celery
from decouple import config
import firebase_admin
from firebase_admin import credentials

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE'))
app = Celery('domtory')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks() ## task.py 이외에서는 ['custom.py'] 이렇게 추가해줘야 함

app.conf.broker_transport_options = {'visibility_timeout': 31536000}

cred_path = config("FIRE_BASE_JSON_KEY_PATH")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, name='celery_firebase_app')
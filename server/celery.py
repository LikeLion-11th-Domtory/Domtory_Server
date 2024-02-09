import os
from celery import Celery
from decouple import config
import firebase_admin
from firebase_admin import credentials

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE'))
app = Celery('domtory')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['push.tasks',])

app.conf.broker_transport_options = {'visibility_timeout': 31536000}

cred_path = config("FIRE_BASE_JSON_KEY_PATH")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, name='celery_firebase_app')

app.conf.broker_connection_retry_on_startup = True


#celery -A server worker -P gevent -c 100 --loglevel=info
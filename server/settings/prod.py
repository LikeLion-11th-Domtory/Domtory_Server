from .base import *
from decouple import config
import pymysql

pymysql.install_as_MySQLdb()
DEBUG = False

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'data/static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

CELERY_BROKER_URL = 'amqp://admin:admin@rabbitmq:5672//'
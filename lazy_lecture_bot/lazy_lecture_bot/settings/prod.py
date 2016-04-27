from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  #, '111.222.333.444', 'mywebsite.com']
DEBUG = False

# Use redis as the celery broker
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

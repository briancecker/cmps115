import dj_database_url
from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500),
}

BLOB_STORAGE_TYPE = "azure"

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "fierce-plains-23392.herokuapp.com"]

# Use redis as the celery broker
BROKER_URL = os.environ["REDISCLOUD_URL"]
CELERY_RESULT_BACKEND = os.environ["REDISCLOUD_URL"]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

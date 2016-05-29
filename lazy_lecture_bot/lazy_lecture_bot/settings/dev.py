from .base import *

DEBUG = True
# Celery configuration
INSTALLED_APPS.append("kombu.transport.django")
BROKER_URL = "django://"

# While in development, don't do async processing.
CELERY_ALWAYS_EAGER = False
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

AWS_STORAGE_BUCKET_NAME = 'lazylecturebot'

from .base import *

DEBUG = True

BLOB_STORAGE_TYPE = "local"

# Celery configuration
INSTALLED_APPS.append("kombu.transport.django")
BROKER_URL = "django://"
# While in development, don't do async processing.
CELERY_ALWAYS_EAGER = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

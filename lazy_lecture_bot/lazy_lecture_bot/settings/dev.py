from .base import *
from modules import file_utilities

DEBUG = True

# Define space to store blob files
# see the wiki for more information: https://github.com/briancecker/cmps115/wiki/Blob-and-Video-Storage/
BLOB_STORAGE_ROOT = os.path.join(file_utilities.TMP_DIR, "BLOB_STORAGE_ROOT")
if not os.path.exists(BLOB_STORAGE_ROOT):
    os.makedirs(BLOB_STORAGE_ROOT)

# Celery configuration
INSTALLED_APPS.append("kombu.transport.django")
BROKER_URL = "django://"
# While in development, don't do async processing.
CELERY_ALWAYS_EAGER = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

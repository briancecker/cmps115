import dj_database_url
from django.utils.crypto import get_random_string
from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500),
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "fierce-plains-23392.herokuapp.com"]

# Use redis as the celery broker
BROKER_URL = os.environ["REDISCLOUD_URL"]
CELERY_RESULT_BACKEND = os.environ["REDISCLOUD_URL"]
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

AWS_STORAGE_BUCKET_NAME = 'lazylecturebot'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Make request.is_secure() work on Heroku
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Need a different secret key for production
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"))

# Use SendGrid addon as an email server
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME", "")
EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", "")
EMAIL_PORT = 25
EMAIL_USE_TLS = False

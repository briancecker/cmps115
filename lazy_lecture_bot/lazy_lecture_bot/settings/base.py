"""
Django settings for lazy_lecture_bot project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'idab6c14ld$-b0fyih3)jyh8*hxh5s68a59acko2-4yy=2o_*6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "main.apps.MainConfig",
    'videoapp',
    's3direct',
    'haystack',
    'elasticsearch',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lazy_lecture_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lazy_lecture_bot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # "ENGINE": 'elasticstack.backends.ConfigurableElasticSearchEngine',
        'URL': os.environ.get('HAYSTACK_URL', 'http://127.0.0.1:8001/'),
        'INDEX_NAME': 'haystack',
        "SETTINGS_NAME": "default",
        'TIMEOUT': 60
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# And one more static files thing... I'm honestly not quite sure I understand this one, but see this link:
#   https://devcenter.heroku.com/articles/django-app-configuration#Whitenoise
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# These are where we'll store uploaded media for now
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# S3 config variables
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

# The region of your bucket, more info:
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
S3DIRECT_REGION = 'us-west-1'

# Destinations in the following format:
# {destination_key: (path_or_function, auth_test, [allowed_mime_types], permissions, custom_bucket)}
#
# 'destination_key' is the key to use for the 'dest' attribute on your widget or model field
S3DIRECT_DESTINATIONS = {
    # Allow anybody to upload any MIME type
    #'misc': ('uploads/misc',),

    # Allow staff users to upload any MIME type
    #'files': ('uploads/files', lambda u: u.is_staff,),

    # Allow anybody to upload jpeg's and png's.
    #'imgs': ('uploads/imgs', lambda u: True, ['image/jpeg', 'image/png'],),

    # Allow authenticated users to upload mp4's
    'vids': ('uploads/vids', lambda u: u.is_authenticated(), ['video/mp4', "video/webm"],),

    # Allow anybody to upload any MIME type with a custom name function, eg:
    #'custom_filename': (lambda original_filename: 'images/unique.jpg',),

    # Specify a non-default bucket for PDFs
    #'pdfs': ('/', lambda u: True, ['application/pdf'], None, 'pdf-bucket',),

    # Allow logged in users to upload any type of file and give it a private acl:
    #'private': (
    #    'uploads/vids',
    #    lambda u: u.is_authenticated(),
    #    '*',
    #    'private'),

    # Allow authenticated users to upload with cache-control for a month and content-disposition set to attachment
    #'cached': (
    #    'uploads/vids',
    #    lambda u: u.is_authenticated(),
    #    '*',
    #    'public-read',
    #    AWS_STORAGE_BUCKET_NAME,
    #    'max-age=2592000',
    #    'attachment')
}

from __future__ import absolute_import

from time import sleep

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lazy_lecture_bot.settings')

from django.conf import settings  # noqa

app = Celery('lazy_lecture_bot')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

"""
WSGI config for lazy_lecture_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import sys

import os

from django.core.wsgi import get_wsgi_application

# https://community.webfaction.com/questions/3553/django-cant-find-my-module
sys.path = [os.path.abspath(os.path.join(__file__, "../.."))] + sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lazy_lecture_bot.settings")

application = get_wsgi_application()

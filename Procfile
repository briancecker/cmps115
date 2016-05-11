web: waitress-serve --port=$PORT lazy_lecture_bot.wsgi:application
worker: celery worker -A lazy_lecture_bot.celery.app

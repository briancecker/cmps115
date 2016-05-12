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

# S3 config variables
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_STORAGE_BUCKET_NAME = 'lazylecturebot'

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
    'vids': ('uploads/vids', lambda u: u.is_authenticated(), ['video/mp4'],),

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
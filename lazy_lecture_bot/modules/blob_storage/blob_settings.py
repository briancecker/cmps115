import boto3
from django.conf import settings

boto3_client = boto3.client("s3")
bucket_name = settings.AWS_STORAGE_BUCKET_NAME

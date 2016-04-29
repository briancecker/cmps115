import json

import boto3
import os
from azure.storage.blob import BlockBlobService
from django.conf import settings
from modules import file_utilities

BLOB_STORAGE_TYPE = getattr(settings, "BLOB_STORAGE_TYPE")
BLOB_STORAGE_ROOT = getattr(settings, "BLOB_STORAGE_ROOT")

if BLOB_STORAGE_TYPE == "local":
    # Define space to store blob files
    # see the wiki for more information: https://github.com/briancecker/cmps115/wiki/Blob-and-Video-Storage/
    if not os.path.exists(BLOB_STORAGE_ROOT):
        os.makedirs(BLOB_STORAGE_ROOT)
elif BLOB_STORAGE_TYPE == "azure":
    def get_credentials():
        if "azure_store_account" not in os.environ or "azure_store_key" not in os.environ:
            with open(file_utilities.abs_resource_path(["credentials", "azure_storage.json"]), "r") as fh:
                dat = json.load(fh)
                return dat["account_name"], dat["key"]
        else:
            return os.environ["azure_store_account"], os.environ["azure_store_key"]

    account, key = get_credentials()
    block_blob_service = BlockBlobService(account_name=account, account_key=key)
elif BLOB_STORAGE_TYPE == "s3":
    boto3_client = boto3.client("s3")

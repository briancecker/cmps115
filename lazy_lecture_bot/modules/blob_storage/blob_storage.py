import hashlib
import os
# Buffer size for reading files chunk by chunk
from azure.storage.file import ContentSettings
from django.utils.datetime_safe import datetime
from django.conf import settings
from main.models import BlobStorage
from modules.blob_storage.blob_settings import block_blob_service

BUF_SIZE = 65536

BLOB_TYPE = getattr(settings, "BLOB_STORAGE_TYPE")
if BLOB_TYPE == "local":
    def _make_bsr_path(file_name):
        current_date = datetime.utcnow()
        date_path = (current_date.year, current_date.month, current_date.day)
        bsr_path = os.path.abspath(os.path.join(getattr(settings, "BLOB_STORAGE_ROOT", None), *map(str, date_path)))
        if not os.path.exists(bsr_path):
            os.makedirs(bsr_path)

        return os.path.join(bsr_path, file_name)


    def store_bsr_data(data, extension=""):
        file_name = data_to_hashed_name(data, extension)
        with open(_make_bsr_path(file_name), 'wb') as fh:
            fh.write(data)

        bs = BlobStorage(file_name=file_name)
        bs.save()

        return bs


elif BLOB_TYPE == "azure":
    def store_bsr_data(data, extension=""):
        file_name = data_to_hashed_name(data, extension)
        block_blob_service.create_blob_from_bytes("blobs", file_name, data,
                                                  content_settings=ContentSettings(content_type='audio/wav'))

        bs = BlobStorage(file_name=file_name)
        bs.save()

        return bs


def data_to_hashed_name(data, extension):
    return hashlib.sha256(data).hexdigest() + "." + extension


def file_to_hashed_name(file):
    """
    Hash an entire file to produce a filesystem compatible filename.
    Taken nearly exactly from http://stackoverflow.com/a/22058673/1392894
    Args:
        file: The file to hash and name

    Returns: Returns the filename

    """
    sha = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)

    return sha.hexdigest()

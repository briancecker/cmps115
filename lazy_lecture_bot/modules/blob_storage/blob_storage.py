import shutil

import os

import hashlib

# Buffer size for reading files chunk by chunk
from django.utils.datetime_safe import datetime
from django.conf import settings

BUF_SIZE = 65536


def store_bsr(file, move_file=True):
    """
    Stores a file in blob storage.
    Args:
        file: The file to store.
        move_file: True to move the file from its old location to the new location in bsr. False to copy the file but
        leave it in the old location as well.

    Returns: A tuple of (year, month, day, file_hash) defining the data needed to retrieve the file at a later time.

    """
    file_name = file_to_hashed_name(file)
    current_date = datetime.utcnow()
    date_path = (current_date.year, current_date.month, current_date.day)
    bsr_path = os.path.abspath(os.path.join(getattr(settings, "BLOB_STORAGE_ROOT", None), *map(str, date_path)))
    if not os.path.exists(bsr_path):
        os.makedirs(bsr_path)

    full_destination_path = os.path.join(bsr_path, file_name)
    if move_file:
        shutil.move(file, full_destination_path)
    else:
        shutil.copy(file, full_destination_path)

    return (*date_path, file_name)


def read_bsr(year, month, day, file_hash):
    """
    Constructs the absolute path to a file in blob storage using it's identifying path components
    Args:
        year: as string, e.g. 2016
        month: as string, e.g. 11 for November, 4 for April
        day: as string, e.g. 5 for the fifth
        file_hash: as a string

    Returns: The absolute path to the file in the BSR

    """
    return os.path.abspath(os.path.join(getattr(settings, "BLOB_STORAGE_ROOT", None), year, month, day, file_hash))


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


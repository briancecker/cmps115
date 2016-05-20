import botocore
import hashlib
from main.models import BlobStorage
from modules.blob_storage import blob_settings

# Buffer size for hashing file to name
BUF_SIZE = 64000


def store_bsr_data(data, extension=None, file_prefix=""):
    """
    Store data into blob storage.
    Args:
        data: The data as a writable bytes string
        extension: The optional file extension
        file_prefix: A file prefix, such as the user id

    Returns: The BlobStorage entry in the database

    """
    file_name = "blob/" + file_prefix + data_to_hashed_name(data, extension)
    blob_settings.boto3_client.put_object(Key=file_name, Body=data, Bucket=blob_settings.bucket_name, ACL="public-read")

    bs = BlobStorage(file_name=file_name)
    bs.save()

    return bs


def create_bsr_from_s3(file_name):
    """
    Create a BlobStorage record from a file already on s3 (such as from a direct s3 upload).
    Args:
        file_name: The name with path of a file on s3

    Returns: The BlobStorage record in the database

    """
    try:
        blob_settings.boto3_client.get_object(Key=file_name, Bucket=blob_settings.bucket_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # Object doesn't exist
            raise FileNotFoundError("{0} does not exist in s3".format(file_name))
        else:
            raise e

    bs = BlobStorage(file_name=file_name)
    bs.save()

    return bs


def data_to_hashed_name(data, extension):
    hash_name = hashlib.sha256(data).hexdigest()
    if extension is not None:
        hash_name += "." + extension

    return hash_name


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

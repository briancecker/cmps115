
def store_bsr(file):
    """
    Stores a file in blob storage. If the file already exists in blob storage, silently returns the identifying
    information without storing a duplicate.
    Args:
        file: The file to store.

    Returns: A tuple of (year, month, day, file_hash) defining the data needed to retrieve the file at a later time.

    """
    pass


def read_bsr(blob_id, identifying_tuple=None):
    """
    Constructs the absolute path to a file in blob storage using either an id or an identifying tuple of ids.
    Args:
        blob_id: The id of the blob as specified in the `blob_id` column of `blob_storage`, ignored if identifying_tuple
        is not None.
        identifying_tuple: The tuple of (year, month, day, file_hash) that uniquely identifies a stored file.

    Returns:

    """


def find_by_hash(file_hash):
    """
    Finds a blob_id based on the file_hash. This may be slow as the database grows.
    Args:
        file_hash: The hash of the file as a string.

    Returns: The blob_id of the stored file
    Raises: FileNotFoundError: if a file with the specified file_hash is not found in blob storage

    """

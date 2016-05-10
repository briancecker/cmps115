import os

from django.test import TestCase
from modules import file_utilities
from modules.blob_storage import blob_storage
from modules.blob_storage import blob_settings


class BlobStorageTest(TestCase):
    def setUp(self):
        # Create a test file we can move and copy
        # http://stackoverflow.com/a/14276423/1392894
        self.test_file = os.path.abspath(os.path.join(file_utilities.TMP_DIR, "blob_storage_test.bin"))
        self.test_file_size = 5120
        with open(self.test_file, 'wb') as fh:
            fh.write(os.urandom(self.test_file_size))
        self.test_file_hash = blob_storage.file_to_hashed_name(self.test_file)

    def tearDown(self):
        os.remove(self.test_file)

    def test_store(self):
        test_bytes = b"This is a test string!"
        bs = blob_storage.store_bsr_data(test_bytes)
        retrieved_bytes = bs.get_blob()
        self.assertEqual(test_bytes, retrieved_bytes)

    def test_store_from_s3(self):
        blob_storage.create_bsr_from_s3("uploads/vids/boy.mp4")

    def test_debug(self):
        print(blob_settings.boto3_client.list_objects(Bucket="lazylecturebot"))
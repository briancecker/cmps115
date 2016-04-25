import os
from django.conf import settings
from django.test import TestCase
from django.utils.datetime_safe import datetime
from main.models import BlobStorage
from modules import file_utilities
from modules.blob_storage import blob_storage


class BlobStorageTest(TestCase):

    def setUp(self):
        self.BSR = getattr(settings, "BLOB_STORAGE_ROOT", None)
        # Create a test file we can move and copy
        # http://stackoverflow.com/a/14276423/1392894
        self.test_file = os.path.abspath(os.path.join(file_utilities.TMP_DIR, "blob_storage_test.bin"))
        self.test_file_size = 5120
        with open(self.test_file, 'wb') as fh:
            fh.write(os.urandom(self.test_file_size))
        self.test_file_hash = blob_storage.file_to_hashed_name(self.test_file)

        # Create test BSR file for reading
        self.test_path = os.path.abspath(os.path.join(self.BSR, "year", "month", "day"))
        if os.path.exists(self.test_path):
            self.fail("Failed to setup! The test path already exists. Please delete BSR/year/month/day")
        os.makedirs(self.test_path)
        self.test_read_file = os.path.join(self.test_path, "test_file")
        self.test_read_contents = os.urandom(self.test_file_size)
        with open(self.test_read_file, 'wb') as fh:
            fh.write(self.test_read_contents)

    def tearDown(self):
        os.remove(self.test_file)
        os.remove(self.test_read_file)
        os.removedirs(self.test_path)

    def test_no_move_store(self):
        blob_storage.store_bsr(self.test_file, move_file=False)
        current_date = datetime.utcnow()
        dir_path = os.path.join(self.BSR, str(current_date.year), str(current_date.month), str(current_date.day))
        hashed_filename = blob_storage.file_to_hashed_name(self.test_file)
        full_path = os.path.join(dir_path, hashed_filename)
        self.assertTrue(os.path.exists(dir_path))
        self.assertTrue(os.path.exists(full_path))
        self.assertTrue(os.path.exists(self.test_file))

        # Check that it's in the database
        blobs = BlobStorage.objects.all()
        self.assertEqual(len(blobs), 1)

        # Remove file from BSR
        print(full_path)
        os.remove(full_path)

    def test_read(self):
        file_path = blob_storage.read_bsr("year", "month", "day", "test_file")
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'rb') as fh:
            contents = fh.read()

        self.assertEqual(self.test_read_contents, contents)

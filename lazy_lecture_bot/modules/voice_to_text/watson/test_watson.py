import os

from django.test import TestCase
from modules import file_utilities
from modules.voice_to_text.watson.voice_to_text import get_credentials, transcribe
from requests import HTTPError


class TestWatson(TestCase):
    def setUp(self):
        try:
            self.credentials = get_credentials()
        except FileNotFoundError:
            self.fail("Missing configuration file for IBM watson credentials. "
                      "Please add json config as resources/config/ibm_watson.json")
        except KeyError:
            self.fail("Malformed configuration file for IBM watson credentials.")

        with open(file_utilities.abs_resource_path(
                ["test_videos", "16Khz_50_sec_audio_cpp_example.mp4.wav"]), "rb") as fh:
            self.test_audio = fh.read()

    def test_transcription(self):
        try:
            transcribe(self.test_audio, self.credentials)
        except HTTPError as e:
            self.fail(str(e))

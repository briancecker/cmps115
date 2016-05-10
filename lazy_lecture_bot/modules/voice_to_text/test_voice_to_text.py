import string
import time

import os
import random
import shutil
from django.test import TestCase, override_settings
from django.utils import timezone
from django.conf import settings
from gunicorn.http.wsgi import create
from main.models import Videos, Segments, Transcripts, BlobStorage, Utterances, Tokens
from modules import file_utilities
from modules.blob_storage import blob_settings
from modules.blob_storage.blob_storage import store_bsr_data, create_bsr_from_s3
from modules.voice_to_text import async_tasks
from modules.voice_to_text.audio_segmenter import AudioSegmenter
from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.max_size_audio_segmenter import MaxSizeAudioSegmenter
from modules.voice_to_text.video_pipeline import VideoPipeline
from modules.voice_to_text.watson.watson_video_pipeline import WatsonVideoPipeline


class RandomSegmenter(AudioSegmenter):
    def __init__(self, n_segments=5):
        self.files = list()
        self.file_size = 5120
        self.n_segments = n_segments

    def cleanup(self):
        """
        Cleanup files
        Returns:

        """
        for f in self.files:
            if os.path.exists(f):
                os.remove(f)

    def segment(self, audio):
        """
        Make some files filled with random data.
        Args:
            audio: audio file

        Returns:

        """
        segment_tuples = list()
        for i in range(1, self.n_segments + 1):
            data = os.urandom(self.file_size)
            segment_tuples.append((data, random.randint(1, 10)))

        return segment_tuples


class RandomTranscriber(AudioTranscriber):
    def __init__(self, n_utterances=5, n_tokens=15):
        super().__init__()
        self.n_utterances = n_utterances
        self.n_tokens = n_tokens

    def transcribe(self, audio):
        result = {"transcript": "The entire segment transcript!",
                  "utterances": list()}
        for _ in range(self.n_utterances):
            utterance = {"transcript": "The utterance transcript",
                         "start": 0.0,
                         "end": 5.0,
                         "tokens": list()}
            for _ in range(self.n_tokens):
                utterance["tokens"].append({"token": ''.join(random.choice(string.ascii_lowercase)
                                                             for _ in range(15)),
                                            "start": 0.0,
                                            "end": 5.0})
            result["utterances"].append(utterance)

        return result


class TestVideoPipeline(TestCase):
    def setUp(self):
        with open(file_utilities.abs_resource_path(["test_videos", "30_sec_cpp_example.mp4"]), "rb") as fh:
            self.test_video = fh.read()

        # Setup fake segmenter and transcriber
        self.n_segments = 10
        self.segmenter = RandomSegmenter(self.n_segments)
        self.transcriber = RandomTranscriber(n_utterances=5, n_tokens=15)

        # Send a test file to s3
        self.test_s3 = "test_s3"
        blob_settings.boto3_client.put_object(Key=self.test_s3, Body=self.test_video,
                                              Bucket=blob_settings.bucket_name, ACL="public-read")
        self.test_blob = create_bsr_from_s3(self.test_s3)

    def tearDown(self):
        self.segmenter.cleanup()
        blob_settings.boto3_client.delete_object(Key=self.test_s3, Bucket=blob_settings.bucket_name)

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       BROKER_BACKEND='memory')
    def test_processing(self):
        vp = VideoPipeline()

        vp.audio_segmenter = self.segmenter
        vp.audio_transcriber = self.transcriber
        video = vp.process_video(self.test_blob)
        self.assertTrue(video is not None)

        # Might take a second for the Celery task to finish
        slept = 0
        while not video.finished_processing and slept < 5:
            time.sleep(1)
            slept += 1
            video.refresh_from_db()

        # Should definitely be finished by now
        self.assertTrue(video.finished_processing)

        # Check that we have the write number of entries everywhere
        self.assertEqual(Videos.objects.count(), 1)
        self.assertEqual(Segments.objects.count(), self.n_segments)
        self.assertEqual(Transcripts.objects.count(), self.n_segments)
        # 2 for the original video and audio + the number of segments made
        self.assertEqual(BlobStorage.objects.count(), 2 + self.n_segments)
        self.assertEqual(Utterances.objects.count(), self.n_segments * self.transcriber.n_utterances)
        self.assertEqual(Tokens.objects.count(),
                         self.n_segments * self.transcriber.n_utterances * self.transcriber.n_tokens)

    def watson_processing(self):
        vp = WatsonVideoPipeline()
        video = vp.process_video(self.test_blob)
        self.assertTrue(video is not None)

        # It might take quite some time for the Celery task to finish. This depends on internet connection.
        slept = 0
        while not video.finished_processing and slept < 120:
            time.sleep(1)
            slept += 1
            video.refresh_from_db()

        # Should definitely be finished by now
        self.assertTrue(video.finished_processing)

        self.assertEqual(Videos.objects.count(), 1)
        self.assertEqual(Segments.objects.count(), 1)
        self.assertEqual(Transcripts.objects.count(), 1)
        self.assertGreater(Utterances.objects.count(), 1)
        self.assertGreater(Tokens.objects.count(), 1)

        # Print some debug text
        print(Transcripts.objects.all()[0].text)
        print(Utterances.objects.all()[0].text)
        print(Tokens.objects.all()[0].text)

    @override_settings(CELERY_ALWAYS_EAGER=True,
                       CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       BROKER_BACKEND='memory')
    def test_async_task(self):
        async_tasks.queue_vp_request(self.test_s3)

        # Should definitely be finished by now
        self.assertEqual(Videos.objects.count(), 1)
        self.assertEqual(Segments.objects.count(), 1)
        self.assertEqual(Transcripts.objects.count(), 1)
        self.assertGreater(Utterances.objects.count(), 1)
        self.assertGreater(Tokens.objects.count(), 1)

        # Print some debug text
        print(Transcripts.objects.all()[0].text)
        print(Utterances.objects.all()[0].text)
        print(Tokens.objects.all()[0].text)


class TestMaxSizeAudioSegmenter(TestCase):
    def test_segment(self):
        segmenter = MaxSizeAudioSegmenter()
        with open(file_utilities.abs_resource_path(
                ["test_videos", "16Khz_50_sec_audio_cpp_example.mp4.wav"]), 'rb') as fh:
            video = fh.read()
        segments = list(segmenter.segment(video))
        # There should only be one segment
        self.assertEqual(len(segments), 1)
        # Segment is around 50 seconds long as it should be
        self.assertLessEqual(segments[0][1] - 50.0, 1.0)

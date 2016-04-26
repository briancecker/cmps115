import string

import os
import random
import shutil
from django.test import TestCase
from django.utils import timezone
from lazy_lecture_bot.settings import BLOB_STORAGE_ROOT
from main.models import Videos, Segments, Transcripts, BlobStorage, Utterances, Tokens
from modules import file_utilities
from modules.voice_to_text.audio_segmenter import AudioSegmenter
from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.max_size_audio_segmenter import MaxSizeAudioSegmenter
from modules.voice_to_text.video_pipeline import VideoPipeline
from tempfile import NamedTemporaryFile


class RandomSegmenter(AudioSegmenter):
    def __init__(self, n_segments):
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
            f = os.path.abspath(os.path.join(file_utilities.TMP_DIR, "test_seg_{0}.bin".format(i)))
            self.files.append(f)
            segment_tuples.append((f, random.randint(1, 10)))
            with open(f, 'wb') as fh:
                fh.write(os.urandom(self.file_size))

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
        test_video = file_utilities.abs_resource_path(["test_videos", "cpp_example.mp4"])

        # Going to move the test_video, so copy it first
        tmp = NamedTemporaryFile(delete=False)
        self.test_video = tmp.name
        shutil.copy(test_video, self.test_video)

        self.n_segments = 10
        self.segmenter = RandomSegmenter(self.n_segments)
        self.transcriber = RandomTranscriber(n_utterances=5, n_tokens=15)

        today = timezone.now()
        self.blob_dir = os.path.join(BLOB_STORAGE_ROOT, str(today.year), str(today.month), str(today.day))
        if os.path.exists(self.blob_dir):
            self.blob_files = os.listdir(self.blob_dir)
        else:
            self.blob_files = None

    def tearDown(self):
        self.segmenter.cleanup()

        # Cleanup extra blob storage files
        if self.blob_files is None:
            shutil.rmtree(self.blob_dir)
        else:
            for f in os.listdir(self.blob_dir):
                if f not in self.blob_files:
                    file_path = os.path.join(self.blob_dir, f)
                    if os.path.exists(file_path):
                        os.remove(file_path)

    def test_processing(self):
        vp = VideoPipeline()

        vp.audio_segmenter = self.segmenter
        vp.audio_transcriber = self.transcriber
        vp.process_video(self.test_video)

        # Check that we have the write number of entries everywhere
        self.assertEqual(Videos.objects.count(), 1)
        self.assertEqual(Segments.objects.count(), self.n_segments)
        self.assertEqual(Transcripts.objects.count(), self.n_segments)
        # 2 for the original video and audio + the number of segments made
        self.assertEqual(BlobStorage.objects.count(), 2 + self.n_segments)
        self.assertEqual(Utterances.objects.count(), self.n_segments * self.transcriber.n_utterances)
        self.assertEqual(Tokens.objects.count(),
                         self.n_segments * self.transcriber.n_utterances * self.transcriber.n_tokens)


class TestMaxSizeAudioSegmenter(TestCase):
    def test_segment(self):
        segmenter = MaxSizeAudioSegmenter()
        video = file_utilities.abs_resource_path(["test_videos", "16Khz_50_sec_audio_cpp_example.mp4.wav"])
        segments = list(segmenter.segment(video))
        # There should only be one segment
        self.assertEqual(len(segments), 1)
        # Segment is around 50 seconds long as it should be
        self.assertLessEqual(segments[0][1] - 50.0, 1.0)

import subprocess
import unittest
import wave

import io
import os
from PIL import Image
from django.test import TestCase
from modules import file_utilities
from modules.blob_storage import blob_storage
from modules.video_processing import screenshotting
from modules.video_processing.video_processing import new_audio_buffer, read_audio_segments_by_time, strip_audio, \
    get_audio_duration, fix_audio


class VideoProcessingTest(TestCase):
    def setUp(self):
        with open(file_utilities.abs_resource_path(["test_videos", "cpp_example.mp4"]), 'rb') as fh:
            self.test_video = fh.read()
        with open(file_utilities.abs_resource_path(["test_videos", "audio_cpp_example.mp4.wav"]), 'rb') as fh:
            self.test_audio = fh.read()

    def test_ffmpeg_exists(self):
        try:
            subprocess.call(["ffmpeg", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                self.fail("ffmpeg not found. Please install ffmpeg.")

    def test_strip_audio(self):
        audio, return_code = strip_audio(self.test_video)
        self.assertEqual(return_code, 0)

        with wave.open(io.BytesIO(audio), 'rb') as wave_read:
            self.assertEqual(wave_read.getframerate(), 16000)
            # This is actually the wrong number of frames because getnframes() seems to have a bug in some cases,
            # but it's consistently wrong in this case..
            self.assertEqual(wave_read.getnframes(), 1073741823)

    def test_bad_wav_fix(self):
        """
        This just shouldn't raise an error
        Returns:

        """
        bad_wavs_dir = file_utilities.abs_resource_path(["test_videos", "bad_wavs"])
        for f in os.listdir(bad_wavs_dir):
            with open(os.path.join(bad_wavs_dir, f), "rb") as fh:
                audio_bytes = fh.read()
                fixed = fix_audio(audio_bytes)
                with wave.open(io.BytesIO(fixed), "rb") as wr:
                    print(wr.getnframes())

    def test_audio_segmenting(self):
        self.assertEqual(len(list(read_audio_segments_by_time(self.test_audio, 14))), 17)

    def test_audio_segment_writing(self):
        for i, segment in enumerate(read_audio_segments_by_time(self.test_audio, 14)):
            try:
                wave_write, _ = new_audio_buffer(self.test_audio)
                wave_write.writeframes(segment)
                wave_write.close()
            except wave.Error as e:
                self.fail("Failed to write audio segments with wave.Error: {0}".format(e))

    def test_get_audio_duration(self):
        duration = get_audio_duration(self.test_audio)
        self.assertLessEqual(duration - 235.937, 0.001)

    def test_take_screenshot(self):
        screenshot, rc = screenshotting.take_screenshot(self.test_video, (0, 0, 0), 250, 140)
        self.assertEqual(rc, 0)
        self.assertEqual(len(screenshot), 4177)
        im = Image.open(io.BytesIO(screenshot))
        self.assertEqual(im.size[0], 250)


if __name__ == "__main__":
    unittest.main()

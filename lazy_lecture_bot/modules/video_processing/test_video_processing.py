import subprocess
import unittest
import wave

import io
import os
from modules import file_utilities


class VideoProcessingTest(unittest.TestCase):
    def test_ffmpeg_exists(self):
        try:
            subprocess.call(["ffmpeg", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                self.fail("ffmpeg not found. Please install ffmpeg.")

    def test_strip_audio(self):
        from modules.video_processing.video_processing import strip_audio
        test_video = file_utilities.abs_resource_path(["test_videos", "cpp_example.mp4"])
        self.assertTrue(os.path.exists(test_video))

        print("reading video...")
        with open(test_video, "rb") as fh:
            video = fh.read()
        print("Done reading video")
        audio, return_code = strip_audio(video)

        self.assertEqual(return_code, 0)

        with wave.open(io.BytesIO(audio), 'rb') as wave_read:
            self.assertEqual(wave_read.getframerate(), 16000)
            self.assertEqual(wave_read.getnframes(), 1073741823)

    def test_audio_segmenting(self):
        from modules.video_processing.video_processing import read_audio_segments_by_time
        test_audio = file_utilities.abs_resource_path(["test_videos", "audio_cpp_example.mp4.wav"])
        self.assertEqual(len(list(read_audio_segments_by_time(test_audio, 14))), 17)

    def test_audio_segment_writing(self):
        from modules.video_processing.video_processing \
            import read_audio_segments_by_time, copy_audio_file_settings

        test_audio = file_utilities.abs_resource_path(["test_videos", "audio_cpp_example.mp4.wav"])
        for i, segment in enumerate(read_audio_segments_by_time(test_audio, 14)):
            audio_out = os.path.join(file_utilities.TMP_DIR, "test_{0}.wav".format(i))
            try:
                wave_write = copy_audio_file_settings(test_audio, audio_out)
                wave_write.writeframes(segment)
                wave_write.close()
                os.remove(audio_out)
            except wave.Error as e:
                self.fail("Failed to write audio segments with wave.Error: {0}".format(e))


if __name__ == "__main__":
    unittest.main()

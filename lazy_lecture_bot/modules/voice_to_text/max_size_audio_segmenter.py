import wave

import sys
from tempfile import NamedTemporaryFile

from modules.video_processing.video_processing import get_audio_params, read_audio_frames, bytes_to_n_frames, \
    copy_audio_file_settings
from modules.voice_to_text.audio_segmenter import AudioSegmenter


class MaxSizeAudioSegmenter(AudioSegmenter):
    def __init__(self, max_size=95):
        """

        Args:
            max_size: Maximum size for each segmented video chunk in megabytes

        Returns:

        """
        super().__init__()
        # Accept max size in megabytes because it's more convenient, but store it in bytes
        self.max_size = max_size * 1024 * 1024

    def segment(self, audio):
        params = get_audio_params(audio)
        # Get base size of an empty bytes object
        empty_bytes_size = sys.getsizeof(b'')
        # Calculate the size of each frame:
        # the number of channels * the number of bytes to represent each channel
        bytes_per_frame = params["nchannels"] * params["sampwidth"]
        # Calculate the target number of frames for each segment
        n_frames = self.max_size - empty_bytes_size // bytes_per_frame

        results = list()
        for segment in read_audio_frames(audio, n_frames):
            frames_in_segment = bytes_to_n_frames(segment, params["nchannels"], params["sampwidth"])
            segment_duration = frames_in_segment / params["framerate"]
            # Assume this will be moved and don't delete
            tmp = NamedTemporaryFile("wb", delete=False)
            # nframes will be adjusted automatically by writeframes. Everything else is the same.
            wave_write = copy_audio_file_settings(audio, tmp.name)
            wave_write.writeframes(segment)
            wave_write.close()

            results.append((tmp.name, segment_duration))

        return results

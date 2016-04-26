from abc import ABCMeta


class AudioSegmenter:
    """
    Abstract class for VideoPipeline.audio_segmenter
    """
    __metaclass__ = ABCMeta

    def segment(self, audio):
        """
        Segment an audio clip into smaller pieces. The size or number of pieces is dependent on the pipeline that
        needs the segmenter.
        Args:
            audio: The path to the audio clip.

        Returns: A list of tuples of (segment_path, segment_duration)

        """
        raise NotImplementedError("Segment is not implemented")

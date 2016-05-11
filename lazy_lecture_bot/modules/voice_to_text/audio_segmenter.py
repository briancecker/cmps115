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
            audio: The audio file loaded as bytes. You might do this by loading the file using open(file, "rb").

        Returns: A list of tuples of (segment, segment_duration), where segment is the segment as an audio file
        as bytes in memory. These bytes can be written using a file opened as open(file, "wb").

        """
        raise NotImplementedError("Segment is not implemented")

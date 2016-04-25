from abc import ABCMeta


class AudioSegmenter:
    """
    Abstract class for VideoPipeline.audio_segmenter
    """
    __metaclass__ = ABCMeta

    def segment(self, audio):
        raise NotImplementedError("Segment is not implemented")

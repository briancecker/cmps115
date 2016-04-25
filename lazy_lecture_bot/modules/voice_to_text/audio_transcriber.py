from abc import ABCMeta


class AudioTranscriber:
    """
    Abstract class for VideoPipeline.audio_transcriber
    """
    __metaclass__ = ABCMeta

    def transcribe(self, audio):
        raise NotImplementedError("transcribe is not implemented")

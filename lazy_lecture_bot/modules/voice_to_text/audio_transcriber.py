from abc import ABCMeta


class AudioTranscriber:
    """
    Abstract class for VideoPipeline.audio_transcriber
    """
    __metaclass__ = ABCMeta

    def transcribe(self, audio):
        """
        Transcribe an audio clip into text.
        Args:
            audio: Path to the audio clip

        Returns:

        """
        raise NotImplementedError("transcribe is not implemented")

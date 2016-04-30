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
            audio: The audio file loaded as bytes. You might do this by loading the file using open(file, "rb").

        Returns: A dictionary describing the transcript as shown in the AudioTranscriber section of the wiki:
            https://github.com/briancecker/cmps115/wiki/Video-Pipeline-Objects
        """
        raise NotImplementedError("transcribe is not implemented")

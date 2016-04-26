from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.max_size_audio_segmenter import MaxSizeAudioSegmenter
from modules.voice_to_text.video_pipeline import VideoPipeline
from modules.voice_to_text.watson.voice_to_text import get_credentials, transcribe_file


class WatsonAudioTranscriber(AudioTranscriber):
    def __init__(self):
        super().__init__()
        self.credentials = get_credentials()

    def transcribe(self, audio):
        transcribe_file(audio, self.credentials)


class WatsonVideoPipeline(VideoPipeline):
    def __init__(self):
        super().__init__()
        self.audio_segmenter = MaxSizeAudioSegmenter(max_size=95)
        self.audio_transcriber = WatsonAudioTranscriber()

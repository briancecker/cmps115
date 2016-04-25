from modules.voice_to_text.audio_segmenter import AudioSegmenter
from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.video_pipeline import VideoPipeline
from modules.voice_to_text.watson.voice_to_text import get_credentials, transcribe_file


class WatsonAudioSegmenter(AudioSegmenter):
    def __init__(self):
        super.__init__()


class WatsonAudioTranscriber(AudioTranscriber):
    def __init__(self):
        super.__init__()
        self.credentials = get_credentials()

    def transcribe(self, audio):
        transcribe_file(audio, self.credentials)


class WatsonVideoPipeline(VideoPipeline):
    def __init__(self):
        self.audio_segmenter = WatsonAudioSegmenter()
        self.audio_transcriber = WatsonAudioTranscriber()
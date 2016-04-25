from modules.voice_to_text.audio_segmenter import AudioSegmenter
from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.video_pipeline import VideoPipeline


class WatsonAudioSegmenter(AudioSegmenter):
    pass


class WatsonAudioTranscriber(AudioTranscriber):
    pass


class WatsonVideoPipeline(VideoPipeline):
    def __init__(self):
        self.audio_segmenter = WatsonAudioSegmenter()
        self.audio_transcriber = WatsonAudioTranscriber()
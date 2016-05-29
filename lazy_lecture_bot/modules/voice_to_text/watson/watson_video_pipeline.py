from modules.voice_to_text.max_size_audio_segmenter import MaxSizeAudioSegmenter
from modules.voice_to_text.video_pipeline import VideoPipeline
from modules.voice_to_text.watson.watson_audio_transcriber import WatsonAudioTranscriber


class WatsonVideoPipeline(VideoPipeline):
    def __init__(self):
        super().__init__()
        self.audio_segmenter = MaxSizeAudioSegmenter(max_size=10)
        self.audio_transcriber = WatsonAudioTranscriber()

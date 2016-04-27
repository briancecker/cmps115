from modules.voice_to_text.audio_transcriber import AudioTranscriber
from modules.voice_to_text.watson.voice_to_text import get_credentials
from modules.voice_to_text.watson.voice_to_text import transcribe_file


class WatsonAudioTranscriber(AudioTranscriber):
    def __init__(self):
        super().__init__()
        self.credentials = get_credentials()

    def transcribe(self, audio):
        watson_transcript = transcribe_file(audio, self.credentials)

        transcript = {"transcript": "", "utterances": list()}
        # transcript is now available, but we need to put it in the right format
        for watson_utterance in watson_transcript["results"]:
            if len(watson_utterance["alternatives"]) > 0:
                # Ignore the alternatives for now, and just take the one with the most confidence (the first)
                watson_utterance = watson_utterance["alternatives"][0]
                watson_tokens = watson_utterance["timestamps"]
                utterance = {"transcript": watson_utterance["transcript"],
                             "start": watson_tokens[0][1],
                             "end": watson_tokens[len(watson_tokens) - 1][2],
                             "tokens": list()}
                for token in watson_tokens:
                    utterance["tokens"].append({"token": token[0], "start": token[1], "end": token[2]})

                transcript["utterances"].append(utterance)

        # Now remake the entire transcript by putting together all the Utterances.
        transcript["transcript"] = " ".join(utterance["transcript"] for utterance in transcript["utterances"])

        return transcript


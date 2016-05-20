import logging

from abc import ABCMeta
from main.models import Segments, Transcripts, Utterances, Tokens
from modules.blob_storage.blob_storage import store_bsr_data
from modules.video_processing import video_processing
from modules.video_processing.video_processing import get_audio_duration

logger = logging.getLogger("django")


class VideoPipelineException(Exception):
    pass


def store_segments(db_video, segments):
    """
    Store each segment in the database.
    Args:
        db_video: The Videos entry
        segments: Each segment as an audio file in memory (bytes)

    Returns: A list of database Segments entries

    """
    db_segments = list()
    for segment_index, (segment, segment_duration) in enumerate(segments):
        audio_blob = store_bsr_data(segment)
        db_segment = Segments(video_id=db_video, segment_index=segment_index,
                              segment_duration=segment_duration,
                              audio_blob=audio_blob)
        db_segment.save()
        db_segments.append(db_segment)

    return db_segments


def store_transcripts(db_video, db_segments, transcripts):
    """
    Store each transcription according to its corresponding segment_id
    Args:
        db_video: The Videos entry of the video that owns these segments
        db_segments: The list of Segments entries that correspond to each transcription
        transcripts: The transcript dictionaries
    Returns: None

    """
    segment_offset = 0.0
    for db_segment, transcript in zip(db_segments, transcripts):
        db_trans = Transcripts(video_id=db_video, segment_id=db_segment, text=transcript["transcript"])
        db_trans.save()
        for utterance_index, utterance in enumerate(transcript["utterances"]):
            db_utterance = Utterances(transcript_id=db_trans, utterance_index=utterance_index,
                                      start_time=segment_offset + utterance["start"],
                                      end_time=segment_offset + utterance["end"],
                                      text=utterance["transcript"])
            db_utterance.save()
            for token_index, token in enumerate(utterance["tokens"]):
                db_token = Tokens(utterance_id=db_utterance, token_index=token_index,
                                  start_time=segment_offset + token["start"],
                                  end_time=segment_offset + token["end"],
                                  text=token["token"])
                db_token.save()

        segment_offset += db_segment.segment_duration


class VideoPipeline:
    """
    Base class for video pipelines.

    Derived classes should provide the following objects:
        self.audio_segmenter: Given an audio file in memory (as bytes), segment it into appropriate sized pieces.
        self.audio_transcriber: Given an audio file in memory (as bytes), return a transcription dictionary.
    """
    __metaclass__ = ABCMeta

    def __init__(self, audio_segmenter=None, audio_transcriber=None):
        self.audio_segmenter = audio_segmenter
        self.audio_transcriber = audio_transcriber

    def _strip_audio(self, video):
        """
        Get the audio from a video

        Args:
            video: The video as bytes

        Returns: audio as bytes

        """
        audio, return_code = video_processing.strip_audio(video)
        if return_code != 0:
            raise VideoPipelineException("ffmpeg returned non-zero error code. Returned code: {0}".format(return_code))

        logger.info("ffmpeg in strip_audio returned return_code: {0}, audio_result is length: {1}".format(return_code,
                                                                                                          len(audio)))

        return audio

    def _store_audio(self, video, audio):
        """
        Store the audio and video data and setup Videos entry in database.
        Args:
            video: incomplete Videos record
            audio: audio as bytes

        Returns: the Videos entry

        """
        audio_blob = store_bsr_data(audio)

        # Need to do something with user_id and finished_processing
        video.audio_blob = audio_blob
        video.save()

    def process_video(self, video):
        """
        Submit a video to be processed by the pipeline. When finished processing, the video will be stored, segmented,
        transcribed, and ready to use. In order to determine if the video is done being processed, check that the
        "finished_processing" field of the Videos entry returned from this function is set to true.
        Args:
            video: The incomplete Videos record. Must have a valid video_blob.

        Returns:

        """
        logger.info("Stripping audio and storing it")
        video.processing_status = "Stripping Audio"
        video.save()
        video_bytes = video.video_blob.get_blob()
        logger.info("Video bytes length: {0}".format(len(video_bytes)))
        audio = self._strip_audio(video_bytes)
        logger.info("Audio is of length {0}".format(len(audio)))
        self._store_audio(video, audio)

        logger.info("Getting video and audio length")
        duration = get_audio_duration(audio)
        video.video_duration = duration

        logger.info("segmenting")
        video.processing_status = "Segmenting Audio"
        video.save()
        audio_segments = self.audio_segmenter.segment(video.audio_blob.get_blob())
        db_segments = store_segments(video, audio_segments)

        logger.info("transcribing {0} segments".format(len(db_segments)))
        video.processing_status = "Transcribing Audio Chunk 1/{0}".format(len(db_segments))
        video.save()
        transcripts = list()
        for i, segment in enumerate(db_segments):
            transcripts.append(self.audio_transcriber.transcribe(segment.audio_blob.get_blob()))
            if i + 1 != len(db_segments):
                video.processing_status = "Transcribing Audio Chunk {0}/{1}".format(i + 2, len(db_segments))
                video.save()

        # transcripts = [self.audio_transcriber.transcribe(segment.audio_blob.get_blob()) for segment in db_segments]
        store_transcripts(video, db_segments, transcripts)

        video.processing_status = ""
        video.finished_processing = True
        video.save()

        logger.info("Done processing video with id: {0}".format(video.id))

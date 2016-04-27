import importlib
from abc import ABCMeta
from lazy_lecture_bot.celery import app
from main.models import Videos, Segments, Transcripts, Utterances, Tokens
from modules.blob_storage.blob_storage import store_bsr
from modules.video_processing import video_processing


class VideoPipelineException(Exception):
    pass


def store_segments(db_video, segments):
    """
    Store each segment in the database.
    Args:
        db_video: The Videos entry
        segments: Each segment as a file path

    Returns: A list of segment ids corresponding to the segments argument

    """
    db_segments = list()
    for segment_index, (segment, segment_duration) in enumerate(segments):
        audio_blob = store_bsr(segment)
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
    Returns:

    """
    for db_segment, transcript in zip(db_segments, transcripts):
        db_trans = Transcripts(video_id=db_video, segment_id=db_segment, text=transcript["transcript"])
        db_trans.save()
        for utterance_index, utterance in enumerate(transcript["utterances"]):
            db_utterance = Utterances(transcript_id=db_trans, utterance_index=utterance_index,
                                      start_time=utterance["start"], end_time=utterance["end"],
                                      text=utterance["transcript"])
            db_utterance.save()
            for token_index, token in enumerate(utterance["tokens"]):
                db_token = Tokens(utterance_id=db_utterance, token_index=token_index, start_time=token["start"],
                                  end_time=token["end"], text=token["token"])
                db_token.save()


def _get_class_information(cls):
    return cls.__module__, cls.__class__.__name__, cls.__dict__


def _construct_from_class_information(cls_info):
    module, class_name, attrs = cls_info
    class_def = getattr(importlib.import_module(module), class_name)
    obj = class_def()
    for key, val in attrs.items():
        setattr(obj, key, val)

    return obj


@app.task(name="process_video_async")
def process_video_async(video_id, audio_segmenter_info, audio_transcriber_info):
    # Construct the segmenter and transcriber we need
    audio_segmenter = _construct_from_class_information(audio_segmenter_info)
    audio_transcriber = _construct_from_class_information(audio_transcriber_info)

    # Get the relevant video and process
    video = Videos.objects.all().get(pk=video_id)
    audio_segments = audio_segmenter.segment(video.audio_blob.get_abs_path())
    # WARNING: self._store_segments will move the audio_segments!
    db_segments = store_segments(video, audio_segments)
    audio_segment_blobs = [db_segment.audio_blob.get_abs_path() for db_segment in db_segments]
    transcripts = [audio_transcriber.transcribe(segment) for segment in audio_segment_blobs]
    store_transcripts(video, db_segments, transcripts)

    video.finished_processing = True
    video.save()

    return "Done async processing video with id: {0}".format(video.id)


class VideoPipeline:
    """
    Base class for video pipelines.

    Derived classes should provide the following objects:
        self.audio_segmenter: Given an audio file, segment it into appropriate sized pieces.
        self.audio_transcriber: Given an audio file, return a transcription dictionary.
    """
    __metaclass__ = ABCMeta

    def __init__(self, audio_segmenter=None, audio_transcriber=None):
        self.audio_segmenter = audio_segmenter
        self.audio_transcriber = audio_transcriber
        self.video = None

    def _strip_audio(self, video):
        """

        Args:
            video:

        Returns: audio from video as a file path

        """
        audio_file, return_code = video_processing.strip_audio(video)
        if return_code != 0:
            raise VideoPipelineException("ffmpeg returned non-zero error code. Returned code: {0}".format(return_code))

        return audio_file

    def _store_video_and_audio(self, video, audio):
        """
        Store the audio and video files and setup Videos entry in database.
        Args:
            video: file path to video
            audio: file path to audio

        Returns: the Videos entry

        """
        video_blob = store_bsr(video)
        audio_blob = store_bsr(audio)

        # Need to do something with user_id and finished_processing
        self.video = Videos(audio_blob=audio_blob, video_blob=video_blob, user_id=1, finished_processing=False)
        self.video.save()

    def process_video(self, video):
        """
        Submit a video to be processed by the pipeline. When finished processing, the video will be stored, segmented,
        transcribed, and ready to use. Some of this processing will run asynchronously, so just because the function
        returns, that does not mean that the video is done processing. In order to determine if the video is done being
        processed, check that the "finished_processing" field of the Videos entry returned from this function is set
        to true.
        Args:
            video: The path to a video file to process.

        Returns: The Videos entry created in the database.

        """
        # Copy for testing. In production this won't be needed
        # tmp = NamedTemporaryFile(delete=False)
        # shutil.copy(video, tmp.name)
        # video = tmp.name

        audio = self._strip_audio(video)
        # WARNING: self._store_video_and_audio will move video and audio files!
        self._store_video_and_audio(video, audio)

        # Can't pass objects directly, so we have to deconstruct the object into interpretable and serializable parts
        process_video_async.delay(self.video.id, _get_class_information(self.audio_segmenter),
                                  _get_class_information(self.audio_transcriber))

        return self.video

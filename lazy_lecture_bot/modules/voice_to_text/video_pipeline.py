from abc import ABCMeta
from main.models import Videos, Segments, Transcripts
from modules.blob_storage.blob_storage import store_bsr
from modules.video_processing import video_processing


class VideoPipelineException(Exception):
    pass


class VideoPipeline:
    """
    Abstract base class for video pipelines.

    Derived classes should provide the following objects:
        audio_segmenter: Given an audio file, segment it into appropriate sized pieces. Derived classes can call
                       VideoPipeline.split_audio(segment_length=x) to help with this task.
        audio_transcriber: Given an audio file, return a transcription dictionary.
    """
    __metaclass__ = ABCMeta

    def __init__(self, audio_segmenter=None, audio_transcriber=None):
        self.audio_segmenter = audio_segmenter
        self.audio_transcriber = audio_transcriber

    def strip_audio(self, video):
        """

        Args:
            video:

        Returns: audio from video as a file path

        """
        audio_file, return_code = video_processing.strip_audio(video)
        if return_code != 0:
            raise VideoPipelineException("ffmpeg returned non-zero error code. Returned code: {0}".format(return_code))

        return audio_file

    def store_video_and_audio(self, video, audio):
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
        video = Videos(audio_blob=audio_blob, video_blob=video_blob, user_id=1, finished_processing=True)
        video.save()
        return video

    def store_segments(self, db_video, segments):
        """
        Store each segment in the database.
        Args:
            db_video: The Videos entry
            segments: Each segment as a file path

        Returns: A list of segment ids corresponding to the segments argument

        """
        db_segments = list()
        for segment_index, segment in enumerate(segments):
            audio_blob = store_bsr(segment)
            db_segment = Segments(video_id=db_video, segment_index=segment_index,
                                  segment_duration=self.audio_transcriber.segment_length,
                                  audio_blob=audio_blob)
            db_segment.save()
            db_segments.append(db_segment)

        return db_segments

    def store_transcripts(self, db_video, db_segments, transcriptions):
        """
        Store each transcription according to its corresponding segment_id
        Args:
            video_id: The video id of the video that owns these segments
            db_segments: The list of Segments entries that correspond to each transcription
            transcriptions: The transcription objects (TODO: should be something other than strings eventually)
        Returns:

        """
        for db_segment, transcript in zip(db_segments, transcriptions):
            db_trans = Transcripts(video_id=db_video, segment_id=db_segment, text=transcript)
            db_trans.save()

    def process_video(self, video):
        audio = self.strip_audio(video)
        db_video = self.store_video_and_audio(video, audio)
        audio_segments = self.audio_segmenter.segment(audio)
        db_segments = self.store_segments(db_video, audio_segments)
        transcriptions = [self.audio_transcriber.transcribe(segment) for segment in audio_segments]
        self.store_transcripts(db_video, db_segments, transcriptions)
        db_video.finished_processing = True
        db_video.save()

        return db_video




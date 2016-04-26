from abc import ABCMeta
from main.models import Videos, Segments, Transcripts
from modules.blob_storage.blob_storage import store_bsr
from modules.video_processing import video_processing


class VideoPipelineException(Exception):
    pass


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
        video = Videos(audio_blob=audio_blob, video_blob=video_blob, user_id=1, finished_processing=True)
        video.save()
        return video

    def _store_segments(self, db_video, segments):
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

    def _store_transcripts(self, db_video, db_segments, transcriptions):
        """
        Store each transcription according to its corresponding segment_id
        Args:
            db_video: The Videos entry of the video that owns these segments
            db_segments: The list of Segments entries that correspond to each transcription
            transcriptions: The transcription objects (TODO: should be something other than strings eventually)
        Returns:

        """
        for db_segment, transcript in zip(db_segments, transcriptions):
            db_trans = Transcripts(video_id=db_video, segment_id=db_segment, text=transcript)
            db_trans.save()

    def process_video(self, video):
        """
        Submit a video to be processed by the pipeline. When finished processing, the video will be stored, segmented,
        transcribed, and ready to use. This function may run asynchronously, so just because the function returns, this
        does not mean that the video is done processing. In order to determine if the video is done being processed,
        check that the "finished_processing" field of the Videos entry returned from this function is set to true.
        Args:
            video: The path to a video file to process.

        Returns: The Videos entry created in the database.

        """
        audio = self._strip_audio(video)
        db_video = self._store_video_and_audio(video, audio)
        audio_segments = self.audio_segmenter.segment(audio)
        db_segments = self._store_segments(db_video, audio_segments)
        transcriptions = [self.audio_transcriber.transcribe(segment[0]) for segment in audio_segments]
        self._store_transcripts(db_video, db_segments, transcriptions)
        db_video.finished_processing = True
        db_video.save()

        return db_video

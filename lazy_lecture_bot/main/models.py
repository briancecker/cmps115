"""
Definition of models.
"""

from django.db import models
# Create your models here.
from django.utils import timezone
from django.conf import settings
from modules.blob_storage import blob_settings


class BlobStorage(models.Model):
    date = models.DateTimeField(default=timezone.now)
    # Restrict all possible file names to only those files in the BLOB_STORAGE_ROOT
    file_name = models.URLField()

    def get_blob(self):
        """
        Get the actual blob object

        Returns: Get the blob as bytes

        """
        blob_type = getattr(settings, "BLOB_STORAGE_TYPE")
        if blob_type == "local":
            import os
            date = self.date
            with open(os.path.abspath(os.path.join(getattr(settings, "BLOB_STORAGE_ROOT", None), str(date.year),
                                                   str(date.month), str(date.day), self.file_name)), 'rb') as fh:
                return fh.read()
        elif blob_type == "azure":
            return blob_settings.block_blob_service.get_blob_to_bytes("blobs", self.file_name)
        elif blob_type == "s3":
            return blob_settings.boto3_client.get_object(Key=self.file_name, Bucket="lazylecturebot")["Body"].read()


class Videos(models.Model):
    audio_blob = models.ForeignKey("BlobStorage", related_name="audio_path")
    video_blob = models.ForeignKey("BlobStorage", related_name="video_path")
    user_id = models.IntegerField()
    # user_id = models.ForeignKey()  # this still needs a path to link to blob_storage user_ID
    finished_processing = models.BooleanField()

    def __unicode__(self):
        return self.video_id


class Segments(models.Model):
    video_id = models.ForeignKey("Videos")
    segment_index = models.IntegerField()
    # Video duration in seconds
    segment_duration = models.FloatField()
    audio_blob = models.ForeignKey("BlobStorage")

    def __unicode__(self):
        return self.segment_id


class Transcripts(models.Model):
    video_id = models.ForeignKey("Videos")
    segment_id = models.ForeignKey("Segments")
    text = models.TextField()

    def __unicode__(self):
        return self.transcript_id


class Utterances(models.Model):
    transcript_id = models.ForeignKey("Transcripts")
    utterance_index = models.IntegerField()
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()


class Tokens(models.Model):
    utterance_id = models.ForeignKey("Utterances")
    token_index = models.IntegerField()
    start_time = models.FloatField()
    end_time = models.FloatField()
    # Possible overkill, but it's there I guess: https://en.wikipedia.org/wiki/Longest_word_in_English
    text = models.CharField(max_length=35)


class Annotation(models.Model):
    video_id = models.ForeignKey("Videos")
    segment_id = models.ForeignKey("Segments")
    word_number = models.IntegerField()
    word_to_url = models.URLField()
    word_id = models.IntegerField()

    def __unicode__(self):
        return self.word_number

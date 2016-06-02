"""
Definition of models.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.utils import timezone
from modules.blob_storage import blob_settings


def get_ghost_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class BlobStorage(models.Model):
    date = models.DateTimeField(default=timezone.now)
    # Restrict all possible file names to only those files in the BLOB_STORAGE_ROOT
    file_name = models.URLField()

    def get_blob(self):
        """
        Get the actual blob object

        Returns: Get the blob as bytes

        """
        return blob_settings.boto3_client.get_object(
            Key=self.file_name, Bucket=blob_settings.bucket_name)["Body"].read()

    def get_url(self):
        """
        Get the url to the blob.
        Returns: if blob storage is "local", return a file system path, otherwise return a ur

        """
        location = blob_settings.boto3_client.get_bucket_location(Bucket="lazylecturebot")["LocationConstraint"]
        return "https://s3-{bucket_location}.amazonaws.com/lazylecturebot/{file_name}".format(
            bucket_location=location, file_name=self.file_name)


class PipelineTypes(models.Model):
    name = models.CharField(max_length=20)


class Videos(models.Model):
    title = models.CharField(max_length=100)
    audio_blob = models.ForeignKey("BlobStorage", related_name="audio_path")
    video_blob = models.ForeignKey("BlobStorage", related_name="video_path")
    user_id = models.IntegerField()
    # user_id = models.ForeignKey()  # this still needs a path to link to blob_storage user_ID
    finished_processing = models.BooleanField()
    processing_status = models.CharField(max_length=20)
    pipeline_type = models.ForeignKey("PipelineTypes")
    video_duration = models.FloatField(default=-1.0)

    def __unicode__(self):
        return self.video_id


class Thumbnail(models.Model):
    video = models.ForeignKey("Videos")
    image_blob = models.ForeignKey("BlobStorage")
    time = models.FloatField()


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
    # Other non-english tokens could also be present, but we have to set the limit somewhere.
    text = models.CharField(max_length=35)


class Annotation(models.Model):
    video_id = models.ForeignKey("Videos")
    segment_id = models.ForeignKey("Segments")
    word_number = models.IntegerField()
    word_to_url = models.URLField()
    word_id = models.IntegerField()

    def __unicode__(self):
        return self.word_number


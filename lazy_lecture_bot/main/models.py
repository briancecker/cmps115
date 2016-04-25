"""
Definition of models.
"""

from django.db import models
# Create your models here.
from django.utils import timezone
from lazy_lecture_bot.settings import BLOB_STORAGE_ROOT


class BlobStorage(models.Model):
    date = models.DateTimeField(default=timezone.now)
    # Restrict all possible file names to only those files in the BLOB_STORAGE_ROOT
    file_name = models.FilePathField(BLOB_STORAGE_ROOT, recursive=True)


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


class Annotation(models.Model):
    video_id = models.ForeignKey("Videos")
    segment_id = models.ForeignKey("Segments")
    word_number = models.IntegerField()
    word_to_url = models.URLField()
    word_id = models.IntegerField()

    def __unicode__(self):
        return self.word_number

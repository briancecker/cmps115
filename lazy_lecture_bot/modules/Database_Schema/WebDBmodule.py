"""
Definition of models.
"""

from django.db import models

# Create your models here.

class videos(models.Model):
    video_id = models.IntegerField(primary_key = True) #primary key

    Audio_Path = models.URLField() 
    Audio_Path = models.ForeignKey() #needs link to blob storage

    Video_Path = models.URLField() 
    Vidio_Path = models.ForeignKey() #needs link to blob storage

    user_ID = models.IntegerField() 
    user_ID = models.ForeignKey() #this still needs a path to link to blob_storage user_ID

    def __unicode__(self):
        return self.video_id


class segments(models.Model):
    class Meta:
        unique_together = ((video_ID,Segment_ID),)

    video_ID = models.IntegerField()
    video_ID = models.ForeignKey(videos.video_id)
    Segment_ID = models.IntegerField()
    Segment_Duration = models.CharField(max_length = 30)
    Audio_Path = models.URLField()
    Video_Path = models.URLField()


    def __unicode__(self):
        return self.Segment_ID


class transcripts(models.Model):
    transcript_ID = models.IntegerField(primary_key = True)
    video_ID = models.ForeignKey(videos.video_id)
    Segment_ID = models.ForeignKey(segments.Segment_ID)
    text = models.TextField()


class annotation(models.Model):
    class Meta:
        unique_together = ((video_ID,Segment_ID,word_id),)

    video_ID = models.IntegerField()
    video_ID = models.ForeignKey(segments.video_ID)
    Segment_ID = models.IntegerField()
    Segment_ID = models.ForeignKey(segments.Segment_ID)
    word_number = models.IntegerField(primary_key = True)
    word_to_url = models.URLField()
    word_id = models.IntegerField()

    def __unicode__(self):
        return self.word_number

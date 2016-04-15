from django.db import models

class segments(models.Model):
    Segment_ID = models.IntegerField()
    Segment_Duration = models.CharField(max_length = 30)
    Audio_Path = models.CharField()
    Video_Path = models.CharField()
    Audio = models.FileField(upload_to)
    Video = models.FileField(upload_to)

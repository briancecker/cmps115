from django.db import models


class videos(models.Model):
    video_id = models.IntegerField(primary_key = True) #primary key
    Audio_Path = models.URLField() #foreign key
    Audio_Path = models.ForeignKey()
    Video_Path = models.URLField() #foreign key
    Audio_Path = models.ForeignKey()
    user_ID = models.IntegerField() #foreign key 

    def __unicode__(self):
        return self.video_id


class segments(models.Model):
    video_ID = models.IntegerField()
    Segment_ID = models.IntegerField()
    Segment_Duration = models.CharField(max_length = 30)
    Audio_Path = models.URLField()
    Video_Path = models.URLField()
    
    def __unicode__():
        return self.Segment_ID

class annotation(models.Model):
    word_number = models.IntegerField(primary_key = True)
    word_to_url = models.URLField()
    word_id = models.IntegerField()

    def __unicode__(self):
        return self.word_number

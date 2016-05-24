from haystack import indexes
from main.models import Transcripts, Utterances, Videos
from videoapp.models import VideoPost


class transcriptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    script = indexes.CharField(model_attr='text')
    segment_id = indexes.IntegerField()
    video_id = indexes.IntegerField()

    def get_model(self):
        return Transcripts

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_segment_id(self, obj):
        return obj.segment_id.id

    def prepare_video_id(self, obj):
        return obj.video_id.id


class UtteranceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    utterance_text = indexes.CharField(model_attr="text")
    utterance_id = indexes.IntegerField(model_attr="id")

    def get_model(self):
        return Utterances

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")
    description = indexes.CharField(model_attr="description")
    author = indexes.CharField()
    video_id = indexes.IntegerField()

    def get_model(self):
        return VideoPost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_author(self, obj):
        return obj.author.username

    def prepare_video_id(self, obj):
        return obj.upload.id
 


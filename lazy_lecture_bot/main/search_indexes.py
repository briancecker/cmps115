from haystack import indexes
from main.models import Transcripts, Utterances


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

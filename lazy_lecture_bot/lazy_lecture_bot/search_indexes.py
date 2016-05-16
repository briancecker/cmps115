from haystack import indexes
from myapp.models import Transcripts

class transcriptIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    script = indexes.CharField(model_attr='text')
    segment_id = indexes.IntegerField(model_attr='segment_id')
    video_id = indexes.IntegerField(model_attr='video_id')

    def get_model(self):
        return Transcript


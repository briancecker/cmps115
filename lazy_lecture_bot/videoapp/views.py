import json
import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from haystack.query import SearchQuerySet
from main.models import Segments, Transcripts, Utterances, Videos
from modules.voice_to_text.async_tasks import queue_vp_request
from .forms import VideoUploadForm
from .models import VideoPost

"""""""""""""""""""""

    WATCH VIDEOS

"""""""""""""""""""""
def watch_video_view(request, videopost_id):
    post = VideoPost.objects.get(pk=videopost_id)
    # data = serializers.serialize("json", Utterances.objects.all())
    video_url = post.upload.video_blob.get_url()

    context = {
        "video_id": post.upload.id,
        "time": time,
        "post": post,
        "video_url": video_url,
        "transcript_data": get_transcript(post.upload),
        "finished_processing": post.upload.finished_processing,
        "processing_status": post.upload.processing_status,
    }
    return render(request, "videoapp/watch_template.html", context)


""""
Helper function that retrieves a list of transcripts when passed a VideoObject.
"""


def get_transcript(video_object):
    results = list()
    print("getting transcripts for video_object with id: {0}".format(video_object.id))
    for segment in video_object.segments_set.order_by("segment_index").all():
        for transcript in segment.transcripts_set.all():
            utterances = transcript.utterances_set.order_by("utterance_index").all()
            add_human_readable_time(utterances)
            results.append({
                "transcript": transcript,
                "utterances": utterances})
    return results


def add_human_readable_time(utterances):

    def hours_mins_secs(secs):
        """
        http://stackoverflow.com/questions/775049/python-time-seconds-to-hms
        """
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        return "{hours}:{mins}:{secs}".format(hours=int(h), mins=int(m), secs=int(s))

    for utterance in utterances:
        utterance.h_start = hours_mins_secs(utterance.start_time)
        utterance.h_end = hours_mins_secs(utterance.end_time)

"""""""""""""""""""""

    UPLOAD VIDEO

"""""""""""""""""""""
@csrf_protect
def upload_view(request):
    form = VideoUploadForm()
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = queue_vp_request(request)

            newpost = VideoPost(upload=video,
                                title=request.POST['title'],
                                description=request.POST['description'],
                                public_access=request.POST['public_access'],
                                author=request.user,
                                upload_duration=''
                                )
            newpost.save()

            return HttpResponseRedirect('/')

    context = {
        'form': form,
    }
    return render(request, "videoapp/upload.html", context)

"""
method that helps with utterance search
"""
@csrf_protect
def search_utterances(request):
    if request.method == "POST":
        video_id = request.POST.get("video_id")
        query = request.POST.get("query")
        videos = Videos.objects.filter(id=video_id)
        if len(videos) == 0:
            return HttpResponse()

        utterance_ids = [utterance_result.utterance_id
                         for utterance_result in SearchQuerySet().models(Utterances).filter(content__startswith=query)]

        return HttpResponse(
            json.dumps({"utterance_ids": utterance_ids}), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({""}), content_type="application/json"
        )

"""""
method that returns the status of the transcript processing
and returns the processesed transcript when finished.
"""""
@csrf_protect
def ajax_transcript_status(request):
    if request.is_ajax():
        v_id = request.POST.get("video_id")
        post = VideoPost.objects.get(pk=v_id)
        # data = serializers.serialize("json", Utterances.objects.all())

        context = {
            "video_id": v_id,
            "post": post,
            "transcript_data": get_transcript(post.upload),
            "finished_processing": post.upload.finished_processing,
            "processing_status": post.upload.processing_status,
        }

        html = render_to_string('videoapp/utterances.html',context, request=request)
        return HttpResponse(html)

"""
Helper Function that returns the duration of a video using the duration of its Segments
"""


def get_video_duration(video_object):
    segment_query = Segments.objects.filter(id=video_object.id)
    duration = 0;
    for segment in segment_query:
        duration += segment.segment_duration

    minutes = int(duration / 60)
    seconds = int(duration % 60)
    converted_time = s_time = str(minutes) + ":" + str(seconds)
    return converted_time

import json
import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from haystack.query import SearchQuerySet
from modules.voice_to_text import async_tasks
from modules.voice_to_text.async_tasks import queue_vp_request
from user.forms import *
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core import serializers
from modules.voice_to_text.watson.watson_video_pipeline import WatsonVideoPipeline
from .forms import VideoUploadForm
from .models import VideoPost
from main.models import Segments, Transcripts, Utterances, Videos

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
    segment_query = Segments.objects.filter(id=video_object.id)
    results = []
    for segment in segment_query:
        transcripts = Transcripts.objects.filter(video_id=video_object.id, segment_id=segment.id)
        if len(transcripts) != 0:
            transcript = transcripts[0]
            utterances = Utterances.objects.filter(transcript_id=transcript.id)
            results.append({
                "transcript": transcript,
                "utterances": utterances})
    return results


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

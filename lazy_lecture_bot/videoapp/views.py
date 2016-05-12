import time

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core import serializers

from modules.voice_to_text.watson.watson_video_pipeline import WatsonVideoPipeline

from .forms import VideoUploadForm
from .models import VideoPost
from main.models import Segments, Transcripts, Utterances

"""""""""""""""""""""

	WATCH VIDEOS

"""""""""""""""""""""
def watch_video_view(request, videopost_id):
	post = VideoPost.objects.get(pk=videopost_id)
	#data = serializers.serialize("json", Utterances.objects.all())
	#print(data)
	#video_url = post.upload.video_blob.get_url()
	video_url = post.upload
	context = {
		"time" : time,
		"post" : post,
		"video_url" : video_url,
		#"transcript_data" : get_transcript(post.upload)
	}
	return render(request, "videoapp/watch_template.html", context)

""""
Helper function that retrieves a list of transcripts when passed a VideoObject.
"""
def get_transcript(video_object):
	segment_query = Segments.objects.filter(id=video_object.id)
	results = []
	segment_begin_offset = 0.0
	for segment in segment_query:
		transcript = Transcripts.objects.filter(video_id=video_object.id, segment_id=segment.id)[0]	
		utterances = Utterances.objects.filter(transcript_id=transcript.id)
		results.append({
			"transcript": transcript,
			"utterances": utterances })
		segment_begin_offset += segment.segment_duration
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
			#pipeline = WatsonVideoPipeline()
			#processed_video = pipeline.process_video( request.FILES['video_file'].read() )
			#video_duration = get_video_duration( processed_video )
			newpost = VideoPost(
								upload = request.POST['video_file'],
								title = request.POST['title'],
								description = request.POST['description'],
								public_access = request.POST['public_access'],
								author = request.user,
								#upload_duration = video_duration
								)
			newpost.save()
			return redirect("watch_video", newpost.id)

	context= {
		'form' : form,
	}
	return render(request, "videoapp/upload.html", context)

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

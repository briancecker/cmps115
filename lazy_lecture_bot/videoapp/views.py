from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect

from modules.voice_to_text.watson.watson_video_pipeline import WatsonVideoPipeline

"""""""""""""""""""""

	WATCH VIDEOS

"""""""""""""""""""""
def watch_video_view(request):
	context = {}
	return render(request, "videoapp/watch_template.html", context)

"""""""""""""""""""""
	
	UPLOAD VIDEO

"""""""""""""""""""""
@csrf_protect
def upload_view(request):
	#pipeline = WatsonVideoPipeline()
	#pipeline.process_video()
	if request.method == "POST":
		video_title = request.POST["title"]
		video_description = request.POST["description"]
		public_access = request.POST["publicAccess"]
		video = request.FILES["uploadedFile"]
	context= {}
	return render(request, "videoapp/upload.html", context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect

from modules.voice_to_text.watson.watson_video_pipeline import WatsonVideoPipeline

from .forms import VideoUploadForm
from .models import VideoPost

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
	form = VideoUploadForm()
	if request.method == "POST":
		#pipeline = WatsonVideoPipeline()
		form = VideoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			newpost = VideoPost(upload = request.FILES['video_file'],
								title = request.POST['title'],
								description = request.POST['description'],
								public_access = request.POST['public_access'],
								author = request.user)
			print(newpost.upload)
			newpost.save()
		#with open(file.temporary_file_path(), 'rb') as f:
		#	pipeline = WatsonVideoPipeline()
		#	what = pipeline.process_video(f.read(file.size))
		#	close(f)
	context= {
		'form' : form,
	}
	return render(request, "videoapp/upload.html", context)
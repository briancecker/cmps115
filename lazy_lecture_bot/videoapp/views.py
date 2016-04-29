from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect

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
	if request.method == "POST":
		video_title = request.POST["title"]
		video_description = request.POST["description"]
		public_permission = request.POST["publicAccess"]
		video = request.POST["uploadedFile"]
		print(video_title)
		print(video_description)
		print(public_permission)
		print(video)
	context= {}
	return render(request, "videoapp/upload.html", context)
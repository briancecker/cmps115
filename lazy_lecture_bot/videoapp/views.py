from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def watch_video_view(request):
	return render(request, "videoapp/watch_template.html", {})

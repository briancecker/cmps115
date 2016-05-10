from django.http import HttpResponse
from django.shortcuts import render
from videoapp.models import VideoPost

def index(request):
	context = {
		"vp" : VideoPost.objects.all().filter(public_access=True),
		"user" : request.user,
		"n" : range(15), # USED FOR TESTING
	}
	return render(request, 'main/index.html', context)

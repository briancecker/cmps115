from django.http import HttpResponse
from django.shortcuts import render
from videoapp.models import VideoPost

def index(request):
	context = {
		"vp" : VideoPost.objects.filter(public_access=True).order_by('publish_date'),
		"user" : request.user,
		"n" : range(15), # USED FOR TESTING
	}
	return render(request, 'main/index.html', context)

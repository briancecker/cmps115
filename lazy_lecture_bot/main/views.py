from django.http import HttpResponse
from django.shortcuts import render
from videoapp.models import VideoPost

def index(request):
	video_list = VideoPost.objects.filter(public_access=True).order_by('publish_date')

	context = {
		"video_list" : video_list,
		"user" : request.user,
	}
	return render(request, 'main/index.html', context)

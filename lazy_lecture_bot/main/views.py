from django.http import HttpResponse
from django.shortcuts import render
from main.models import Thumbnail
from videoapp.models import VideoPost

def index(request):
	vps = VideoPost.objects.filter(public_access=True).order_by('publish_date')
	add_image_urls(vps)
	context = {
		"vp" : vps,
		"user" : request.user,
	}
	return render(request, 'main/index.html', context)


def add_image_urls(video_posts):
	"""
	Add the urls to the thumbnail to each VideoPost
	Args:
	    video_posts: list of VideoPost objects

	Returns:

	"""
	for vp in video_posts:
		thumbs = Thumbnail.objects.filter(video = vp.upload.id)
		if len(thumbs) > 0:
			vp.thumb_url = thumbs[0].image_blob.get_url()
		else:
			vp.thumb_url = "https://placeholdit.imgix.net/~text?txtsize=23&txt=250%C3%97140&w=254&h=140"

from django.db import models
from main.models import Videos
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_ghost_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/videos/<filename>
    return 'user_{0}/videos/{1}'.format(instance.author.id, filename)

# Create your models here.
class VideoPost(models.Model):
	"""Model that aggregates the metadata of the video post"""
	upload = models.ForeignKey('main.Videos')
	title = models.CharField(max_length = 50)
	description = models.CharField(max_length = 455)
	public_access = models.BooleanField()
	publish_date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey( settings.AUTH_USER_MODEL,
								on_delete=models.SET(get_ghost_user))
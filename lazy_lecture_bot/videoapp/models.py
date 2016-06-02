from django.db import models
from main.models import Videos, get_ghost_user
from django.conf import settings
from django.utils import timezone


# Create your models here.
class VideoPost(models.Model):
    """Model that aggregates the metadata of the video post"""
    upload = models.ForeignKey('main.Videos')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=455)
    public_access = models.BooleanField()
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_ghost_user))
    upload_duration = models.CharField(max_length=6)

    def _add_image_urls(self):
        """
        Add the urls to the thumbnail
        Returns:

        """
        thumbs = self.upload.thumbnail_set.all()
        if len(thumbs) > 0:
            return thumbs[0].image_blob.get_url()
        else:
            return "https://placeholdit.imgix.net/~text?txtsize=23&txt=250%C3%97140&w=254&h=140"

    thumb_url = property(_add_image_urls)

    def _favorited_by(self):
        """
        Convenience set that shows which users favorited a video. Useful for templates that need to check if the
        logged-in user has favorited a video.
        Returns: A set of all user's (by id) that have favorited this VideoPost

        """
        favorites = self.favorite_set.all()
        if len(favorites) > 0:
            return set(fav.user.id for fav in favorites)
        else:
            return set()

    favorited_by = property(_favorited_by)


class Favorite(models.Model):
    video_post = models.ForeignKey("VideoPost")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_ghost_user))


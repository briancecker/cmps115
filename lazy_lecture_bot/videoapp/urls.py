from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.watch_video_view, name="watch"),
]
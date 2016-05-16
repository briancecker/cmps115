from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.watch_video_view, name="watch"),
    url(r'^(?P<videopost_id>[0-9]+)/$', views.watch_video_view, name="watch_video"),
]

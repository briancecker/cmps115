from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.watch_video_view, name="watch"),
    url(r'^upload/', views.upload_view, name="upload"),
    url(r'^search_utterances/', views.search_utterances, name="search_utterances"),
    url(r'^favorite_video/$', views.favorite_video, name="favorite_video"),
    url(r'^(?P<videopost_id>[0-9]+)/$', views.watch_video_view, name="watch_video"),
    url(r'^transcript_status/', views.ajax_transcript_status, name='transcript_status'),
    url(r"^favorite_video/", views.favorite_video, name="favorite_video"),
]

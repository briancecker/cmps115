from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.show_user),
    url(r'^(?P<username>[\w.@+-]+)$', views.show_user, name="profile"),
    url(r'^(?P<username>[\w.@+-]+)/update/$', views.update_user), # Doesn't work yet
    url(r'^(?P<username>[\w.@+-]+)/delete/$', views.delete_user), # Doesn't work yet
]

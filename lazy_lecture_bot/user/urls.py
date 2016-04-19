from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.show_user),
    url(r'^login/$', views.login_user), # Doesn't work yet
    url(r'^update/$', views.update_user), # Doesn't work yet
    url(r'^delete/$', views.delete_user), # Doesn't work yet
    url(r'^logoff/$', views.logoff_user), # Doesn't work yet
    url(r'^(?P<username>[\w.@+-]+)$', views.show_user, name="profile"),
]

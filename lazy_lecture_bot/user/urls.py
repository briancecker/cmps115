from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.show_user),
    url(r'^(?P<username>[\w.@+-]+)$', views.show_user, name="profile"),
    url(r'^create/$', views.create_user),
    url(r'^login/$', views.login_user),
    url(r'^update/$', views.update_user),
    url(r'^delete/$', views.delete_user),
    url(r'^logoff/$', views.logoff_user),
]

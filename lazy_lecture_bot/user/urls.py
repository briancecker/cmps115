from django.conf.urls import url

from . import views

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', views.show_user),
    url(r'^(?P<username>[\w.@+-]+)$', views.show_user, name="profile"),
    url(r'^signup/', views.signup_view, name="signup"),
    url(r'^logoff/', views.logoff_user, name="logoff"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^login/auth_login/$', views.auth_login, name="auth_login"),
    url(r'^(?P<username>[\w.@+-]+)/update/$', views.update_user), # Doesn't work yet
    url(r'^(?P<username>[\w.@+-]+)/delete/$', views.delete_user), # Doesn't work yet
]

"""lazy_lecture_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from lazy_lecture_bot import initial_data_loading
from user import views as user_views
from videoapp import views as video_views
from haystack.views import SearchView

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^$', include('main.urls'), name="main"),
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^u/', include('user.urls')),
    url(r'^signup/', user_views.signup_view, name="signup"),
    url(r'^logoff/', user_views.logoff_user, name="logoff"),
    url(r'^login/$', user_views.login_user, name="login"),
    url(r'^login/auth_login/$', user_views.auth_login, name="auth_login"),
    url(r'^watch/', include('videoapp.urls'), name="video_watch"),
    url(r'^upload/', video_views.upload_view, name="upload"),
    url(r'^search_utterances/', video_views.search_utterances, name="search_utterances"),
    url(r'^s3direct/', include('s3direct.urls')),
    url(r'^search/', SearchView('search/search.html'), name='haystack_search')
]


# urls.py is only ever loaded once, so it's a good place for one-off startup loading
def startup():
    initial_data_loading.import_data()


startup()

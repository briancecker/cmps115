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
from haystack.views import SearchView

urlpatterns = [
    # map sends the default index page to be mapped by the main app
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^u/', include('user.urls')),
    url(r'^watch/', include('videoapp.urls'), name="video_watch"),
    url(r'^s3direct/', include('s3direct.urls')),
    url(r'^search/', SearchView('search/search.html'), name='haystack_search'),
    url(r'^', include('main.urls'), name="main"),
]


# urls.py is only ever loaded once, so it's a good place for one-off startup loading
def startup():
    initial_data_loading.import_data()


startup()

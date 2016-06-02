from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r"^favorites/$", views.favorites, name="favorites"),
   url(r"^subscriptions/$", views.subscriptions, name="subscriptions"),
]

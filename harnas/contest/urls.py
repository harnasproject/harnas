from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='contest_index'),
    url(r'^([0-9]+)$', views.details, name='contest_details'),
    url(r'^new/$', views.new, name='contest_new'),
]
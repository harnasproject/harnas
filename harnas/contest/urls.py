from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='contest_index'),
    url(r'^(?P<id>\d+)/$', views.details, name='contest_details'),
    url(r'^new/$', views.edit, name='contest_new'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='contest_edit'),
]
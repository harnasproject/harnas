from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contest/$', views.index, name='contest_index'),
    url(r'^contest/(?P<id>\d+)/$', views.details, name='contest_details'),
    url(r'^contest/new/$', views.edit, name='contest_new'),
    url(r'^contest/edit/(?P<id>\d+)/$', views.edit, name='contest_edit'),
    url(r'^task/$', views.task_index, name='task_index'),
    url(r'^task/(?P<id>\d+)/$', views.task_details, name='task_details'),
    url(r'^task/new$', views.task_edit, name='task_new'),
    url(r'^task/edit/(?P<id>\d+)/$', views.task_edit, name='task_edit'),
]

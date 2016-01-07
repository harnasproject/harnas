from django.conf.urls import url
from harnas.contest.views import contest, task

urlpatterns = [
    url(r'^contest/$', contest.index, name='contest_index'),
    url(r'^contest/(?P<id>\d+)/$', contest.details, name='contest_details'),
    url(r'^contest/new/$', contest.edit, name='contest_new'),
    url(r'^contest/edit/(?P<id>\d+)/$', contest.edit, name='contest_edit'),
    url(r'^task/$', task.index, name='task_index'),
    url(r'^task/(?P<id>\d+)/$', task.details, name='task_details'),
    url(r'^task/new$', task.edit, name='task_new'),
    url(r'^task/edit/(?P<id>\d+)/$', task.edit, name='task_edit'),
    url(r'^contest/(?P<id>\d+)/news/new', contest.add_news, name='add_news'),
    url(r'^news/delete/(?P<id>\d+)', contest.delete_news, name='delete_news'),
    url(r'^news/edit/(?P<id>\d+)', contest.edit_news, name='edit_news'),
]

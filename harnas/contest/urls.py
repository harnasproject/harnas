from django.conf.urls import url
from harnas.contest.views import contest, task, news, groups

urlpatterns = [
    url(r'^contest/$', contest.index, name='contest_index'),
    url(r'^contest/(?P<id>\d+)/$', contest.details, name='contest_details'),
    url(r'^contest/new/$', contest.edit, name='contest_new'),
    url(r'^contest/edit/(?P<id>\d+)/$', contest.edit, name='contest_edit'),
    url(r'^task/$', task.index, name='task_index'),
    url(r'^task/(?P<id>\d+)/$', task.details, name='task_details'),
    url(r'^task/new$', task.edit, name='task_new'),
    url(r'^task/edit/(?P<id>\d+)/$', task.edit, name='task_edit'),
    url(r'^task/(?P<id>\d+)/upload_file/$', task.upload_file, name='task_upload_file'),
    url(r'^task/(?P<id>\d+)/download_file/$', task.download_file, name='task_download_file'),
    url(r'^task/(?P<id>\d+)/delete_file/$', task.delete_file, name='task_delete_file'),
    url(r'^contest/(?P<id>\d+)/news/new/$', news.new, name='news_add'),
    url(r'^news/delete/(?P<id>\d+)/$', news.delete, name='news_delete'),
    url(r'^news/edit/(?P<id>\d+)/$', news.edit, name='news_edit'),
    url(r'^groups/new/(?P<contest_id>\d+)/$', groups.new, name='groups_new'),
]

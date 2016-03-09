from django.conf.urls import url
from harnas.contest.views import contest, task, news, groups

urlpatterns = [
    url(r'^contest/$', contest.index, name='contest_index'),
    url(r'^contest/new/$', contest.edit, name='contest_new'),
    url(r'^contest/(?P<id>\d+)/$', contest.details, name='contest_details'),
    # contest_fetch_task must be before contest_details with tabs
    url(r'^contest/(?P<id>\d+)/fetch_task/$', contest.fetch_task, name='contest_fetch_task'),
    url(r'^contest/(?P<id>\d+)/(?P<tab>\w+)/$', contest.details, name='contest_details'),
    url(r'^contest/(?P<id>\d+)/edit/$', contest.edit, name='contest_edit'),
    url(r'^contest/(?P<contest_id>\d+)/groups/new/$', groups.new, name='contest_group_new'),
    url(r'^contest/(?P<contest_id>\d+)/groups/(?P<group_id>\d+)/edit/$', groups.view, name='contest_group_edit'),
    url(r'^contest/(?P<contest_id>\d+)/groups/(?P<group_id>\d+)/delete/$', groups.delete, name='contest_group_delete'),
    url(r'^contest/(?P<contest_id>\d+)/groups/(?P<group_id>\d+)/tasks/(?P<task_id>\d+)/edit/$',
        groups.edit_task_details, name='contest_task_details_edit'),
    url(r'^contest/(?P<contest_id>\d+)/news/new/$', news.new, name='contest_news_new'),
    url(r'^contest/(?P<contest_id>\d+)/news/(?P<news_id>\d+)/edit/$', news.edit, name='contest_news_edit'),
    url(r'^contest/(?P<contest_id>\d+)/news/(?P<news_id>\d+)/delete/$', news.delete, name='contest_news_delete'),

    url(r'^task/$', task.index, name='task_index'),
    url(r'^task/(?P<id>\d+)/$', task.details, name='task_details'),
    url(r'^task/new$', task.edit, name='task_new'),
    url(r'^task/edit/(?P<id>\d+)/$', task.edit, name='task_edit'),
    url(r'^task/(?P<id>\d+)/upload_file/$', task.upload_file, name='task_upload_file'),
    url(r'^task/(?P<id>\d+)/download_file/$', task.download_file, name='task_download_file'),
    url(r'^task/(?P<id>\d+)/delete_file/$', task.delete_file, name='task_delete_file'),
]

from django.conf.urls import include, url
from harnas.contest.views import contest, groups, news, submit, task, testcase

task_urlpatterns = [
    url(r'^$',
        task.index,
        name='task_index'),
    url(r'^new$',
        task.new,
        name='task_new'),
    url(r'^(?P<task_id>\d+)/', include([
        url(r'^$',
            task.details,
            name='task_details'),
        url(r'^edit/$',
            task.edit,
            name='task_edit'),
        url(r'^upload_file/$',
            task.upload_file,
            name='task_upload_file'),
        url(r'^download_file/$',
            task.download_file,
            name='task_download_file'),
        url(r'^delete_file/$',
            task.delete_file,
            name='task_delete_file'),
        url(r'^testcase/', include([
            url(r'^new/$',
                testcase.new,
                name='testcase_new'),
            url(r'^edit/(?P<testcase_id>\d+)/',
                testcase.edit,
                name='testcase_edit'),
        ]))
    ])),
]

contest_urlpatterns = [
    url(r'^$',
        contest.index,
        name='contest_index'),
    url(r'^new/$',
        contest.edit,
        name='contest_new'),
    url(r'^(?P<contest_id>\d+)/', include([
        url(r'^$',
            contest.details,
            name='contest_details'),
        url(r'^fetch_task/$',
            contest.fetch_task,
            name='contest_fetch_task'),
        url(r'^edit/$',
            contest.edit,
            name='contest_edit'),
        url(r'^submit/$',
            contest.submit,
            name='contest_submit'),
        url(r'^save_submit/$',
            contest.save_submit,
            name='contest_save_submit'),
        url(r'^groups/', include([
            url(r'^new/$',
                groups.new,
                name='contest_group_new'),
            url(r'^(?P<group_id>\d+)/', include([
                url(r'^$',
                    groups.view,
                    name='contest_group_details'),
                url(r'^delete/$',
                    groups.delete,
                    name='contest_group_delete'),
                url(r'^tasks/(?P<task_id>\d+)/edit/$',
                    groups.edit_task_details,
                    name='contest_task_details_edit'),
            ])),
        ])),
        url(r'^news/', include([
            url(r'^new/$',
                news.new,
                name='contest_news_new'),
            url(r'^(?P<news_id>\d+)/', include([
                url(r'^edit/$',
                    news.edit,
                    name='contest_news_edit'),
                url(r'^delete/$',
                    news.delete,
                    name='contest_news_delete'),
            ]))
        ])),
    ])),
]

urlpatterns = [
    url(r'^contest/', include(contest_urlpatterns)),
    url(r'^task/', include(task_urlpatterns)),
    url(r'^submit/(?P<id>\d+)/$',
        submit.details,
        name='submit_details'),
]

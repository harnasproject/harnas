from django.conf.urls import include, url
from harnas.checker.views import checker, cluster, template, test_environment

test_environment_urlpatterns = [
    url(r'^$',
        test_environment.index,
        name='test_environment_index'),
    url(r'^new$',
        test_environment.edit,
        name='test_environment_new'),
    url(r'^(?P<id>\d+)/$',
        test_environment.details,
        name='test_environment_details'),
    url(r'^(?P<id>\d+)/edit$',
        test_environment.edit,
        name='test_environment_edit'),
]

urlpatterns = [
    url(r'^status/$', cluster.status, name='cluster_status'),
    url(r'^template/$', template.index, name='template_index'),
    url(r'test_environment/', include(test_environment_urlpatterns)),
    url(r'^hera_callback/', include([
        url(r'^submit/(?P<submit_id>\d+)/$',
            checker.check,
            name='checker_check'),
    ])),
]

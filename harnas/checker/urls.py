from django.conf.urls import url
from harnas.checker.views import cluster, template, test_environment

urlpatterns = [
    url(r'^status/$', cluster.status, name='cluster_status'),
    url(r'^template/$', template.index, name='template_index'),
    url(r'^test_environment/$',
        test_environment.index,
        name='test_environment_index'),
    url(r'^test_environment/(?P<id>\d+)/$',
        test_environment.details,
        name='test_environment_details'),
    url(r'^test_environment/new$',
        test_environment.edit,
        name='test_environment_new'),
    url(r'^test_environment/edit/(?P<id>\d+)/$',
        test_environment.edit,
        name='test_environment_edit'),
]

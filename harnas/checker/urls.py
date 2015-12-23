from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^status/$', views.status, name='checker_status'),
]

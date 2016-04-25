from django.conf.urls import url
from harnas.userprofile import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.show, name='account_profile'),
    url(r'^settings/$', views.edit, name='account_settings'),
]

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages import views

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^checker/', include('harnas.checker.urls')),
    url(r'^', include('harnas.contest.urls')),
]

urlpatterns += [
  url(r'^about/$', views.flatpage, { 'url': '/about/' }, name='about'),
  url(r'^authors/$', views.flatpage, { 'url': '/authors/'}, name='authors'),
  url(r'^$', views.flatpage, { 'url': '/'}, name='homepage'),
]

from django.conf.urls import include, url

from harnas.customregistration.views import RegistrationView

urlpatterns = [
    # redirect registration requests to custom view
    url(r'^register/$', RegistrationView.as_view()),
    url(r'^', include('registration.backends.default.urls')),
]

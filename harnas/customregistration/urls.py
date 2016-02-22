from django.conf.urls import include, url
from harnas.customregistration.views import *

urlpatterns = [
    # auth patterns to prevent grappelli from overriding them
    url(
        r'^login/$',
        login_override,
        name='login'
    ),
    url(
        r'^logout/$',
        logout_override,
        name='logout'
    ),
    url(
        r'^password/reset/done/$',
        password_reset_done_override,
        name='password_reset_done'
    ),
    url(
        r'^reset/done/$',
        password_reset_complete_override,
        name='password_reset_complete'
    ),
    url(
        r'^password/change/done/$',
        password_change_done_override,
        name='password_change_done'
    ),

    # redirect registration requests to custom view (displaying messages)
    url(
        r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'
    ),
    # redirects activation requests to custom view (displaying messages)
    url(
        r'^activate/complete/$',
        activation_complete_override,
        name='registration_activation_complete'
    ),
    url(
        r'^',
        include('registration.backends.default.urls')
    )
]
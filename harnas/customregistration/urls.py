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
        r'^password/reset/$',
        password_reset_override,
        name='password_reset'
    ),
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{'
        r'1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm_override,
        name='password_reset_confirm'
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
        r'^password/change/$',
        password_change_override,
        name='password_change'
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

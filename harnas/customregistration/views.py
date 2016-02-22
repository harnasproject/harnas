from django.contrib import messages
from django.contrib.auth.views import password_reset, password_reset_confirm, \
    password_change, login, logout

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from registration.backends.default import views


def login_override(request):
    """
    Change default login view to display message after successful login.
    """
    response = login(
        request,
        template_name='custom_login.html'
    )
    # Base login method returns HttpResponseRedirect upon successful login
    if request.method == 'POST' and isinstance(response, HttpResponseRedirect):
        messages.add_message(request, messages.SUCCESS, _('You are now logged in.'))
    return response


def logout_override(request, next_page=None):
    """
    Change default logout view to display message after successful logout.
    """
    response = logout(request, next_page)
    if not isinstance(response, HttpResponseRedirect):
        messages.add_message(request, messages.SUCCESS, _('You have been logged out.'))
        return HttpResponseRedirect(reverse('homepage'))
    else:
        return response


def password_reset_done_override(request):
    messages.add_message(request, messages.INFO, _(
        'We have sent you an email with a link to reset your password.'))
    return HttpResponseRedirect(reverse('homepage'))


def password_reset_complete_override(request):
    messages.add_message(request, messages.SUCCESS,
                         _('Your password has been reset. You can log in.'))
    return HttpResponseRedirect(reverse('auth_login'))


def password_change_done_override(request):
    messages.add_message(request, messages.SUCCESS,
                         _('Your password has been changed!'))
    return HttpResponseRedirect(reverse('account_settings'))


def activation_complete_override(request):
    messages.add_message(request, messages.SUCCESS,
                         _('Your account is now activated. You can log in.'))
    return HttpResponseRedirect(reverse('login'))


class RegistrationView(views.RegistrationView):
    """
    Overrode Registration view for handling initial user profile data saving
    during registration.
    """

    def register(self, request, form):
        user = super(RegistrationView, self).register(request, form)

        user.userprofile.date_of_birth = form.cleaned_data['date_of_birth']
        user.userprofile.organization = form.cleaned_data['organization']
        user.userprofile.save()
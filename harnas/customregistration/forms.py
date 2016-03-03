from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from registration.forms import RegistrationFormUniqueEmail
from registration.users import UsernameField

from harnas.userprofile.models import UserProfile


class RegistrationForm(RegistrationFormUniqueEmail):
    """
    Custom registration form that adds fields used in user profile.
    """

    date_of_birth = forms.DateField(
        initial=now
    )
    organization = forms.ChoiceField(
        choices=UserProfile.ORGANIZATION_CHOICES,
        initial='H'
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', UsernameField())

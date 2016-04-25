from datetime import date

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from harnas.userprofile.models import UserProfile
from registration.forms import RegistrationFormUniqueEmail
from registration.users import UsernameField


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
    sex = forms.ChoiceField(
        choices=UserProfile.SEX_CHOICES,
        initial='M'
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', UsernameField())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        date_of_birth = cleaned_data.get("date_of_birth")

        today = date.today()
        delta = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        if delta < 10:
            raise forms.ValidationError("You need to be at least 10 years old to use this website.")

        if delta > 110:
            raise forms.ValidationError("Provided date of birth is invalid.")

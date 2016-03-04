from django import forms
from django.contrib.auth.models import User

from harnas.userprofile.models import UserProfile


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('organization', 'personal_page', 'show_email', 'show_age')


class UserFieldsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

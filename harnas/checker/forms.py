from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from harnas.checker.utils import get_templates_list
from harnas.checker.models import TestEnvironment, Submit
from harnas.contest.models import Task


class TestEnvironmentForm(ModelForm):

    template_name = forms.ChoiceField(
        choices=lambda: [(template.id, template.name)
                         for template in get_templates_list()])
    maintainer = forms.ModelChoiceField(
        queryset=User.objects.exclude(username='AnonymousUser'),
        empty_label=None)

    class Meta:
        model = TestEnvironment
        fields = ['summary', 'description']


class SubmitForm(forms.Form):
    solution = forms.FileField(label="Upload your solution")
    task = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        contest = kwargs.pop('contest')
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(contest=contest)

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from harnas.checker.utils import get_templates_list
from harnas.checker.models import TestEnvironment
from harnas.contest.models import Task
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


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

    def clean(self):
        solution = self.cleaned_data['solution']
        max_solution_size = self.cleaned_data['task'].max_solution_size
        if solution._size > max_solution_size:
            error_message = 'You cannot upload files larger than %(max_size)s.'
            max_size = filesizeformat(max_solution_size)
            raise forms.ValidationError(_(error_message),
                                        params={'max_size': max_size},
                                        code='too_large_solution')

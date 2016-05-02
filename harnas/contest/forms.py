from django import forms
from django.contrib.auth.models import Group
from django.forms import Form, ModelForm
from django.utils.timezone import now, timedelta
from harnas.contest.models import (Contest, GroupTaskDetails, News, Task,
                                   TestCase)


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ['max_memory', 'max_duration']


class UploadFileForm(Form):
    file = forms.FileField(label="Upload new file")


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'short_name', 'description', 'test_environment',
                  'max_solution_size']


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description']


class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'description']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class TaskDetailsForm(ModelForm):
    class Meta:
        model = GroupTaskDetails
        fields = ['open', 'deadline', 'close']


class TaskFetchForm(Form):
    task = forms.ModelChoiceField(queryset=Task.objects.filter(parent=None),
                                  empty_label=None)

    open = forms.DateTimeField(initial=now)
    deadline = forms.DateTimeField(initial=(lambda: now() + timedelta(days=7)))
    close = forms.DateTimeField(initial=(lambda: now() + timedelta(days=14)))

    def clean(self):
        cleaned_data = super(TaskFetchForm, self).clean()

        date_open = cleaned_data.get("open")
        date_deadline = cleaned_data.get("deadline")
        date_close = cleaned_data.get("close")

        if not date_open < date_deadline < date_close:
            raise forms.ValidationError("Dates must be in order open < " +
                                        "deadline < close.")

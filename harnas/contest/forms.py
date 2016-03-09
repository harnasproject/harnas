from django.utils.timezone import now, timedelta
from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import Group


from harnas.contest.models import TestCase, Task, News, Contest, GroupTaskDetails


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ['task', 'max_memory', 'max_duration', 'comparator',
                  'executor', 'comparator', 'in_file_path', 'out_file_path']


class UploadFileForm(Form):
    file = forms.FileField(label="Upload new file")


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'short_name', 'description', 'test_environment']


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
            raise forms.ValidationError("Dates must be in order open < deadline < close.")


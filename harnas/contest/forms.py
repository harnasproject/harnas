from django import forms
from django.forms import Form, ModelForm
from django.contrib.auth.models import Group


from harnas.contest.models import TestCase, Task, News, Contest


class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ['task', 'max_memory', 'max_duration', 'comparator',
                  'executor', 'comparator', 'in_file_path', 'out_file_path']


class UploadFileForm(forms.Form):
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


class TaskFetchForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects.filter(parent=None),
                                  empty_label=None)


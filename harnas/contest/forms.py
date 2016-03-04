from django import forms
from django.forms import ModelForm


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
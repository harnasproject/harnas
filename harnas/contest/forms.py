from django import forms
from django.forms import ModelForm
from harnas.contest import models


class ContestForm(ModelForm):

    class Meta:
        model = models.Contest
        fields = ['name', 'description']


class NewsForm(ModelForm):

    class Meta:
        model = models.News
        fields = ['title', 'description']


class TaskForm(ModelForm):

    class Meta:
        model = models.Task
        fields = ['name', 'short_name', 'description', 'test_environment']


class TestCaseForm(ModelForm):

    class Meta:
        model = models.TestCase
        fields = ['task', 'max_memory', 'max_duration', 'comparator',
                  'executor', 'comparator', 'in_file_path', 'out_file_path']


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload new file")

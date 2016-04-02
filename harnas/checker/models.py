from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from harnas.checker.utils import get_templates_list
from harnas.contest.models import Task

class TestEnvironment(models.Model):
    template_name = models.CharField(max_length=250)
    summary = models.CharField(max_length=250)
    description = models.TextField()
    maintainer = models.ForeignKey(User)

    class Meta:
        permissions = (
            ('view_test_environment', 'Can view test environment'),
            ('edit_test_environment', 'Can edit test environment'))

    def __str__(self):
        return self.template_name


class TestEnvironmentForm(ModelForm):

    template_name = forms.ChoiceField(
        choices=lambda: [(template.id, template.name) for template in get_templates_list()])
    maintainer = forms.ModelChoiceField(
        queryset=User.objects.exclude(username='AnonymousUser'),
        empty_label=None)

    class Meta:
        model = TestEnvironment
        fields = ['summary', 'description']


class Submit(models.Model):
    QUEUED = "QUE"
    MEMORY_LIMIT = "MEM"
    TIME_LIMIT = "TLE"
    ACCEPTED = "OK"
    INTERNAL_ERROR = "INT"
    WRONG_ANSWER = "ANS"
    COMPILATION_ERROR = "CMP"
    RUNTIME_ERROR = "RTE"
    STATUS_CHOICES = (
        (QUEUED, "In checking queue"),
        (MEMORY_LIMIT, "Memory limit exceeded"),
        (TIME_LIMIT, "Time limit exceeded"),
        (ACCEPTED, "Accepted"),
        (INTERNAL_ERROR, "Internal error"),
        (WRONG_ANSWER, "Wrong answer"),
        (COMPILATION_ERROR, "Compilation error"),
        (RUNTIME_ERROR, "Runtime error"),
    )

    submitter = models.ForeignKey(User)
    submitted = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('contest.Task')
    solution = models.BinaryField()
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES)


class SubmitForm(ModelForm):
    solution = forms.FileField(label="Upload your solution")
    task = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        contest = kwargs.pop('contest')
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(contest=contest)

    class Meta:
        model = Submit
        fields = []

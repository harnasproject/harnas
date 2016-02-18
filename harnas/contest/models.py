from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from harnas.checker.models import TestEnvironment
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# test_case_fs = FileSystemStorage(location=settings.TEST_CASE_STORAGE_PREFIX)


class Contest(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)

    class Meta:
        permissions = (
            ('view_contest', 'Can view'),
            ('participate_in_contest', 'Can participate'),
            ('manage_contest', 'Can manage contest'))

    def __str__(self):
        return self.name


class ContestForm(ModelForm):

    class Meta:
        model = Contest
        fields = ['name', 'description']


class News(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)

    class Meta:
        verbose_name_plural = "news"

    def __str__(self):
        return self.title


class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'description']


class Task(models.Model):
    name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=3)
    description = models.TextField()
    test_environment = models.ForeignKey(TestEnvironment)
    author = models.ForeignKey(User)

    class Meta:
        permissions = (
            ('view_task', 'Can view task'),
            ('submit_solution', 'Can submit solution'),
            ('edit_task', 'Can edit task'))

    def __str__(self):
        return self.name


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'short_name', 'description', 'test_environment']


class TestCase(models.Model):
    task = models.ForeignKey(Task)
    max_memory = models.PositiveIntegerField()
    max_duration = models.PositiveIntegerField()
    comparator = models.CharField(max_length=500)
    executor = models.CharField(max_length=500)
    in_file_path = models.CharField(max_length=500)
    out_file_path = models.CharField(max_length=500)


class TestCaseForm(ModelForm):

    class Meta:
        model = TestCase
        fields = ['task', 'max_memory', 'max_duration', 'comparator',
                  'executor', 'comparator', 'in_file_path', 'out_file_path']

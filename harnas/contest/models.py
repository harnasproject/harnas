from django.contrib.auth.models import User
from django.db import models
from harnas.checker.models import TestEnvironment


class Contest(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False)
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


class TestCase(models.Model):
    task = models.ForeignKey(Task)
    max_memory = models.PositiveIntegerField()
    max_duration = models.PositiveIntegerField()
    comparator = models.CharField(max_length=500)
    executor = models.CharField(max_length=500)
    in_file_path = models.CharField(max_length=500)
    out_file_path = models.CharField(max_length=500)

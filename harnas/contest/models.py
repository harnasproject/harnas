from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        permissions = (
            ('view', 'Can view'),
            ('participant', 'Can participate'),
            ('manager', 'Can manage contest'))

class News(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField()
    author = models.ForeignKey(User)
    contest_id = models.ForeignKey(Contest)

class TestEnvironment(models.Model):
    template_name = models.CharField(max_length=250)

class Task(models.Model):
    name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=3)
    description = models.TextField()
    test_environment = models.ForeignKey(TestEnvironment)

class TestCase(models.Model):
    task = models.ForeignKey(Task)
    max_memory = models.PositiveIntegerField()
    max_duration = models.PositiveIntegerField()


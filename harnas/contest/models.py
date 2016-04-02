from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from harnas.contest import helpers


import os


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
    test_environment = models.ForeignKey('checker.TestEnvironment')
    author = models.ForeignKey(User)
    parent = models.ForeignKey('self', null=True, default=None)
    contest = models.ForeignKey(Contest, null=True, default=None)

    # Default timestamps values for task. Can be overridden individually in
    # groups. See GroupsTaskDetails.
    open = models.DateTimeField(null=True, default=None)
    deadline = models.DateTimeField(null=True, default=None)
    close = models.DateTimeField(null=True, default=None)

    class Meta:
        permissions = (
            ('view_task', 'Can view task'),
            ('submit_solution', 'Can submit solution'),
            ('edit_task', 'Can edit task'))

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        if self.contest is not None and self.contest.name.strip() != "":
            return "%s (%s)" % (self.name, self.contest.name)
        else:
            return self.name


@receiver(post_save,
          sender=Task,
          dispatch_uid="make_directory_for_task_files")
def make_directory_for_task_files(sender, instance, **kwargs):
    if kwargs['created']:
        task_dir = os.path.join(settings.TASK_STORAGE_PREFIX, str(instance.pk))
        if instance.parent:
            parent_dir = os.path.join(settings.TASK_STORAGE_PREFIX,
                                      str(instance.parent.pk))
            helpers.copy_directory(parent_dir, task_dir)
        else:
            os.mkdir(task_dir)


class TestCase(models.Model):
    task = models.ForeignKey(Task)
    max_memory = models.PositiveIntegerField()
    max_duration = models.PositiveIntegerField()
    comparator = models.CharField(max_length=500)
    executor = models.CharField(max_length=500)
    in_file_path = models.CharField(max_length=500)
    out_file_path = models.CharField(max_length=500)


class GroupTaskDetails(models.Model):
    group = models.ForeignKey(Group, null=False)
    task = models.ForeignKey(Task, null=False)

    open = models.DateTimeField()
    deadline = models.DateTimeField()
    close = models.DateTimeField()

    class Meta:
        index_together = ['group', 'task']

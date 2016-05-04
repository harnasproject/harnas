import os

import shutil
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from harnas.contest import helpers


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
    max_solution_size = models.PositiveIntegerField()

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


class TaskFilesDirectoryError(Exception):
    pass


@receiver(post_save,
          sender=Task,
          dispatch_uid="make_directory_for_task_files")
def make_directory_for_task_files(sender, instance, **kwargs):
    task_dir = os.path.join(settings.TASK_STORAGE_PREFIX, str(instance.pk))
    if os.path.exists(task_dir):
        return
    if instance.parent:
        fetch_task_files(task_dir, instance.parent.pk)
    else:
        make_task_dir(task_dir)


def fetch_task_files(task_dir: str, source_task_id: int) -> None:
    parent_dir = os.path.join(settings.TASK_STORAGE_PREFIX,
                              str(source_task_id))
    try:
        helpers.copy_directory(parent_dir, task_dir)
    except Exception as e:
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
        raise TaskFilesDirectoryError(
            'Unable to copy task files: %s' % e)


def make_task_dir(task_dir: str) -> None:
    try:
        os.mkdir(task_dir)
    except Exception as e:
        raise TaskFilesDirectoryError(
            'Unable to make directory for task files: %s' % e)


class TestCase(models.Model):
    QUEUED = "QUE"
    MEMORY_LIMIT = "MEM"
    TIME_LIMIT = "TLE"
    ACCEPTED = "OK"
    INTERNAL_ERROR = "INT"
    WRONG_ANSWER = "ANS"
    COMPILATION_ERROR = "CME"
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

    task = models.ForeignKey(Task)
    name = models.CharField(max_length=100, null=True, default=None)
    max_memory = models.PositiveIntegerField()
    max_duration = models.PositiveIntegerField()
    run_order_id = models.PositiveSmallIntegerField(default=0)
    comparator = models.CharField(max_length=500)
    executor = models.CharField(max_length=500)
    in_file_path = models.FilePathField(max_length=500)
    out_file_path = models.FilePathField(max_length=500)

    def __str__(self):
        return self.name


class GroupTaskDetails(models.Model):
    group = models.ForeignKey(Group, null=False)
    task = models.ForeignKey(Task, null=False)

    open = models.DateTimeField()
    deadline = models.DateTimeField()
    close = models.DateTimeField()

    class Meta:
        index_together = ['group', 'task']

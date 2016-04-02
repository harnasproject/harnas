from django.contrib.auth.models import User
from django.db import models


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

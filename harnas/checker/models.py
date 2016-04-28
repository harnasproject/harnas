from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from harnas.contest.models import TestCase


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
    submitter = models.ForeignKey(User)
    submitted = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('contest.Task')
    solution = models.BinaryField()
    status = models.CharField(max_length=3,
                              choices=TestCase.STATUS_CHOICES)
    webhook_secret = models.CharField(
                        max_length=settings.WEBHOOK_SECRET_LENGTH)

    def __str__(self):
        return self.id

    def change_status(self, status):
        if status not in [choice[0] for choice in TestCase.STATUS_CHOICES]:
            raise ValueError("Invalid status")
        else:
            self.status = status
            self.save()

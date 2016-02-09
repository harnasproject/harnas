from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from harnas.checker.utils import get_templates_list


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

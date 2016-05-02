from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from harnas.contest.forms import TestCaseForm
from harnas.contest.models import Task, TestCase


@require_POST
@login_required
def new(request, task_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    return handle_testcase_form(request, task, TestCase())


@require_POST
@login_required
def edit(request, task_id, testcase_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    testcase = TestCase.objects.get(pk=testcase_id)
    return handle_testcase_form(request, task, testcase)


def handle_testcase_form(request, task, testcase):
    form = TestCaseForm(request.POST, instance=testcase)
    if form.is_valid():
        testcase = form.save(commit=False)
        testcase.task = task
        testcase.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Testcase %s saved successfully.' % testcase)
    return HttpResponseRedirect(reverse('task_details', args=[task.pk]) +
                                '?current_tab=test_cases')

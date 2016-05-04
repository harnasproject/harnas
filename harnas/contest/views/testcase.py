import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from harnas.contest.forms import TestCaseForm
from harnas.contest.helpers import save_testcase_file, get_task_dir
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
    form = TestCaseForm(request.POST, request.FILES, instance=testcase)
    if form.is_valid():
        testcase = form.save(commit=False)
        testcase.task = task
        testcase.run_order_id = TestCase.objects.filter(
                                    task_id__exact=task.pk).count()
        handle_testcase_files(testcase,
                              request.FILES['in_file'],
                              request.FILES['out_file'])
        testcase.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Testcase %s saved successfully.' % testcase)
    return HttpResponseRedirect(reverse('task_details', args=[task.pk]) +
                                '?current_tab=test_cases')


def handle_testcase_files(testcase, in_file, out_file):
    testcase.in_file_path = in_file
    testcase.out_file_path = out_file
    testcase_dir = os.path.join(get_task_dir(testcase.task.pk), testcase.name)
    if not os.path.exists(testcase_dir):
        os.mkdir(testcase_dir)
    save_testcase_file(in_file, testcase_dir)
    save_testcase_file(out_file, testcase_dir)

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from guardian.shortcuts import assign_perm, get_objects_for_user

from harnas.checker.forms import SubmitForm
from harnas.contest.forms import TaskForm, UploadFileForm, TestCaseForm
from harnas.contest.helpers import save_task
from harnas.contest.models import Task

task_filesystem = FileSystemStorage(location=settings.TASK_STORAGE_PREFIX)


@require_safe
@login_required
def index(request):
    is_contest_manager = \
        get_objects_for_user(request.user,
                             'contest.manage_contest').count() > 0
    if (
        not request.user.has_perm('contest.add_contest') and
        not is_contest_manager
    ):
        raise PermissionDenied
    tasks = Task.objects.filter(parent=None)
    return render(request, 'contest/task_index.html', {'tasks': tasks})


@require_safe
@login_required
def details(request, task_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.view_task', task):
        raise PermissionDenied
    if request.user.has_perm('contest.edit_task', task):
        task_path = str(task_id)
        task_files = task_filesystem.listdir(task_path)[1]
        upload_file_form = UploadFileForm()
        testcase_form = TestCaseForm()
    if request.user.has_perm('contest.submit_solution', task):
        submit_form = SubmitForm(contest=task.contest)
    testcases = task.testcase_set.all()

    return render(request, 'contest/task_details.html', {
        'task': task,
        'task_files': task_files,
        'upload_file_form': upload_file_form,
        'submit_form': submit_form,
        'testcase_form': testcase_form,
        'testcases': testcases,
    })


@require_http_methods(['GET', 'POST'])
@login_required
def new(request):
    form_post = reverse('task_new')
    if not request.user.has_perm('contest.add_task'):
        raise PermissionDenied

    def new_task_assign_perm(task):
        assign_perm('contest.edit_task', request.user, task)
        assign_perm('contest.view_task', request.user, task)

    return handle_task_form(request, form_post, Task(),
                            success_action=new_task_assign_perm)


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, task_id):
    assert task_id is not None

    task = Task.objects.get(pk=task_id)
    form_post = reverse('task_edit', args=[task_id])
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied

    def invalidate_task_cache(task):
        cache_key = make_template_fragment_key('task_description', [task.pk])
        cache.delete(cache_key)

    return handle_task_form(request, form_post, task,
                            success_action=invalidate_task_cache)


def handle_task_form(request, form_post, task, success_action):
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.author_id:
                task.author_id = request.user.pk
            if save_task(task):
                success_action(task)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Task %s saved successfully.' % task)
                return HttpResponseRedirect(
                    reverse('task_details', args=[task.pk]))
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Unable to save this task. '
                    'Please report this accident to administrator.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'contest/task_new.html', {
        'form': form,
        'form_post': form_post
    })


@require_http_methods(['POST'])
@login_required
def upload_file(request, task_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['file']
        task_path = str(task_id) + '/'
        task_filesystem.save(task_path + file.name, file)
    return HttpResponseRedirect(reverse('task_details',
                                        args=[task.pk]))


@require_safe
@login_required
def download_file(request, task_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    task_path = str(task_id) + '/'
    filename = request.GET.get('filename', None)
    file_path = task_path + filename
    file_exists = False
    if filename is not None:
        file_exists = task_filesystem.exists(file_path)
    if not file_exists:
        raise Http404
    file = task_filesystem.open(task_path + filename)
    response = HttpResponse(file, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file.name
    return response


@require_safe
@login_required
def delete_file(request, task_id):
    task = Task.objects.get(pk=task_id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    task_path = str(task_id) + '/'
    filename = request.GET.get('filename', None)
    file_path = task_path + filename
    file_exists = False
    if filename is not None:
        file_exists = task_filesystem.exists(file_path)
    if not file_exists:
        raise Http404
    task_filesystem.delete(file_path)
    return HttpResponseRedirect(reverse('task_details',
                                        args=[task.pk]))

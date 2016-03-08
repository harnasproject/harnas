from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from harnas.contest.models import Task
from harnas.contest.forms import TaskForm, UploadFileForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings


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
def details(request, id):
    task = Task.objects.get(pk=id)
    if not request.user.has_perm('contest.view_task', task):
        raise PermissionDenied
    if request.user.has_perm('contest.edit_task', task):
        task_path = str(id)
        task_files = task_filesystem.listdir(task_path)[1]
        upload_file_form = UploadFileForm()
    return render(request, 'contest/task_details.html',
                  { 'task': task, 
                    'task_files': task_files,
                    'upload_file_form': upload_file_form })


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, id=None):
    if id:
        task = Task.objects.get(pk=id)
        form_post = reverse('task_edit', args=[id])
        if not request.user.has_perm('contest.edit_task', task):
            raise PermissionDenied
    else:
        task = Task()
        form_post = reverse('task_new')
        if not request.user.has_perm('contest.add_task'):
            raise PermissionDenied
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(instance=task)
    if form.is_valid():
        new_task = form.save(commit=False)
        if id is None:
            new_task.author_id = request.user.pk
        new_task.save()
        assign_perm('contest.edit_task', request.user, new_task)
        assign_perm('contest.view_task', request.user, new_task)
        cache_key = make_template_fragment_key('task_description',
                                               [new_task.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('task_details',
                                            args=[new_task.pk]))
    return render(request, 'contest/task_new.html',
                  { 'form': form,
                    'form_post': form_post })


@require_http_methods(['POST'])
@login_required
def upload_file(request, id):
    task = Task.objects.get(pk=id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['file']
        task_path = str(id) + '/'
        task_filesystem.save(task_path + file.name, file)
    return HttpResponseRedirect(reverse('task_details',
                                        args=[task.pk]))


@require_safe
@login_required
def download_file(request, id):
    task = Task.objects.get(pk=id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    task_path = str(id) + '/'
    filename = request.GET.get('filename', None)
    file_path = task_path + filename
    file_exists = False if filename is None else task_filesystem.exists(file_path)
    if not file_exists:
        raise Http404
    file = task_filesystem.open(task_path + filename)
    response = HttpResponse(file, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file.name
    return response

@require_safe
@login_required
def delete_file(request, id):
    task = Task.objects.get(pk=id)
    if not request.user.has_perm('contest.edit_task', task):
        raise PermissionDenied
    task_path = str(id) + '/'
    filename = request.GET.get('filename', None)
    file_path = task_path + filename
    file_exists = False if filename is None else task_filesystem.exists(file_path)
    if not file_exists:
        raise Http404
    task_filesystem.delete(file_path)
    return HttpResponseRedirect(reverse('task_details',
                                        args=[task.pk]))

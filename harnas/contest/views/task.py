from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from guardian.decorators import permission_required
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from harnas.contest.models import Task, TaskForm


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
    tasks = Task.objects.all()
    return render(request, 'contest/task_index.html', {'tasks': tasks})


@require_safe
@login_required
def details(request, id):
    task = Task.objects.get(pk=id)
    if not request.user.has_perm('contest.view_task', task):
        raise PermissionDenied
    return render(request, 'contest/task_details.html', {'task': task})


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

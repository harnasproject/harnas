from django.shortcuts import render
from .models import Contest, ContestForm, Task, TaskForm
from guardian.decorators import permission_required
from django.views.decorators.http import require_safe, require_http_methods
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import assign_perm
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


@require_safe
def index(request):
    return render(request, 'contest/index.html')


def get_contest_and_form(request, id=None):
    if id:
        contest = Contest.objects.get(pk=id)
    else:
        contest = Contest()
    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
    else:
        form = ContestForm(instance=contest)
    return (contest, form)


@require_safe
@permission_required('contest.view', (Contest, 'id', 'id'))
def details(request, id):
    (contest, form) = get_contest_and_form(request, id)
    return render(request, 'contest/details.html', { 'contest': contest, 'form': form })


@require_http_methods(['GET', 'POST'])
def edit(request, id=None):
    (contest, form) = get_contest_and_form(request, id)
    if id is None:
        if not request.user.has_perm('contest.add_contest'):
            raise PermissionDenied
    else:
        if not request.user.has_perm('contest.manage', contest):
            raise PermissionDenied
    if form.is_valid():
        new_contest = form.save(commit=False)
        if id is None:
            new_contest.creator_id = request.user.pk
        new_contest.save()
        assign_perm('contest.manage', request.user, new_contest)
        assign_perm('contest.view', request.user, new_contest)
        cache_key = make_template_fragment_key('contest_description', [new_contest.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('contest_details', args=(new_contest.pk,)))
    return render(request, 'contest/new.html', { 'form': form })


@require_safe
def task_index(request):
    tasks = Task.objects.all()
    return render(request, 'contest/task_index.html', {'tasks': tasks})


@require_safe
def task_details(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'contest/task_details.html', {'task': task})

@require_http_methods(['GET', 'POST'])
def task_edit(request, id=None):
    if id:
        task = Task.objects.get(pk=id)
    else:
        task = Task()
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(instance=task)
    if form.is_valid():
        new_task = form.save(commit=False)
        if id is None:
            new_task.author_id = request.user.pk
            new_task.test_environment_id = 1
        new_task.save()
        cache_key = make_template_fragment_key('task_description', [new_task.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('task_details', args=(new_task.pk,)))
    return render(request, 'contest/task_new.html', {'form': form})

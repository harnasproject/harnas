from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from guardian.decorators import permission_required
from guardian.shortcuts import assign_perm
from harnas.contest.models import Task, TaskForm


@require_safe
def index(request):
    tasks = Task.objects.all()
    return render(request, 'contest/task_index.html', {'tasks': tasks})


@require_safe
def details(request, id):
    task = Task.objects.get(pk=id)
    return render(request, 'contest/task_details.html', {'task': task})


@require_http_methods(['GET', 'POST'])
def edit(request, id=None):
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
        new_task.save()
        cache_key = make_template_fragment_key('task_description', [new_task.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('task_details', args=(new_task.pk,)))
    return render(request, 'contest/task_new.html', {'form': form})

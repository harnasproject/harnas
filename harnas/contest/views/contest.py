from datetime import datetime

from copy import deepcopy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from guardian.shortcuts import get_groups_with_perms
from harnas.contest.forms import GroupForm
from guardian.shortcuts import assign_perm, get_users_with_perms
from harnas.contest.models import Contest, Task, GroupTaskDetails
from harnas.contest.forms import ContestForm, NewsForm, TaskFetchForm
from harnas.utils import permission_denied_message
from harnas.checker.forms import SubmitForm
from harnas.checker.models import Submit


@require_safe
def index(request):
    return render(request, 'contest/contest_index.html')


@require_safe
@login_required
def details(request, contest_id):
    current_tab = request.GET.get('current_tab', 'news')

    contest = Contest.objects.get(pk=contest_id)
    if not request.user.has_perm('contest.view_contest', contest):
        permission_denied_message(request)
        return HttpResponseRedirect('/')

    contest_form = ContestForm(instance=contest)

    groups = get_groups_with_perms(contest, attach_perms=True)
    groups = [k for k, v in groups.items() if 'view_contest' in v]
    group_form = GroupForm()

    news_set = contest.news_set.all().order_by('-created_at')
    news_form = NewsForm()

    fetch_task_form = TaskFetchForm()

    participants = []
    if request.user.has_perm('contest.manage_contest', contest):
        participants = get_users_with_perms(contest, attach_perms=True)
        participants = [k for k, v in participants.items()
                        if 'participate_in_contest' in v]

    tasks = Task.objects.filter(contest=contest)

    return render(request, 'contest/contest_details.html', {
        'contest': contest,
        'contest_form': contest_form,
        'groups': groups,
        'group_form': group_form,
        'participants': participants,
        'news_set': news_set,
        'news_form': news_form,
        'fetch_task_form': fetch_task_form,
        'tasks': tasks,
        'current_tab': current_tab,
    })


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, contest_id=None):
    if contest_id:
        contest = Contest.objects.get(pk=contest_id)
        form_post = reverse('contest_edit', args=[contest_id])
        if not request.user.has_perm('contest.manage_contest', contest):
            permission_denied_message(request)
            return HttpResponseRedirect('/')
    else:
        contest = Contest()
        form_post = reverse('contest_new')
        if not request.user.has_perm('contest.add_contest'):
            permission_denied_message(request)
            return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
    else:
        form = ContestForm(instance=contest)
    if form.is_valid():
        new_contest = form.save(commit=False)
        new_contest.slug = slugify(new_contest.name)
        if contest_id is None:
            new_contest.creator_id = request.user.pk
        new_contest.save()
        assign_perm('contest.manage_contest', request.user, new_contest)
        assign_perm('contest.view_contest', request.user, new_contest)
        cache_key = make_template_fragment_key('contest_description',
                                               [new_contest.pk])
        cache.delete(cache_key)
        messages.add_message(request,
                             messages.SUCCESS,
                             "Contest has been successfully updated.")
        return HttpResponseRedirect(reverse('contest_details',
                                            args=[new_contest.pk]))

    messages.add_message(request,
                         messages.SUCCESS,
                         "Contest has been successfully created.")
    return render(request, 'contest/contest_new.html', {
        'form': form,
        'form_post': form_post
    })


@require_POST
@login_required
def fetch_task(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    if not request.user.has_perm('manage_contest', contest):
        permission_denied_message(request)
    elif request.method == 'POST':
        form = TaskFetchForm(request.POST)
        if form.is_valid():
            parent_task = form.cleaned_data['task']
            fetched_task = deepcopy(parent_task)
            fetched_task.pk = None
            fetched_task.contest = contest
            fetched_task.parent = parent_task
            fetched_task.open = form.cleaned_data['open']
            fetched_task.deadline = form.cleaned_data['deadline']
            fetched_task.close = form.cleaned_data['close']
            fetched_task.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "New task has been added to contest %s."
                                 % contest.name)
            # add tasks to groups
            for group in get_groups_with_perms(contest, attach_perms=True):
                GroupTaskDetails.objects.create(task=fetched_task,
                                                group=group,
                                                open=fetched_task.open,
                                                deadline=fetched_task.deadline,
                                                close=fetched_task.close)

    return HttpResponseRedirect(reverse('contest_details',
                                        args=[contest_id, 'tasks']))


@require_safe
@login_required
def submit(request, contest_id):
    task_id = request.GET.get('task_id', None)
    contest = Contest.objects.get(pk=contest_id)
    submit_form = SubmitForm(contest=contest,
                             initial={'task': task_id})
    return render(request, 'contest/contest_submit.html', {
        'submit_form': submit_form,
        'contest_id': contest_id,
    })


@require_http_methods(['POST'])
@login_required
def save_submit(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST, request.FILES, contest=contest)
        print(str(request.FILES))
        if submit_form.is_valid():
            submit = Submit()
            submit.submitter = request.user
            submit.task = submit_form.cleaned_data['task']
            submit.solution = bytes(request.FILES['solution'].read())
            submit.status = Submit.QUEUED
            submit.save()
            return HttpResponseRedirect(reverse('submit_details',
                                                args=[submit.pk]))
    return render(request, 'contest/contest_submit.html', {
        'submit_form': submit_form,
        'contest_id': contest_id,
    })

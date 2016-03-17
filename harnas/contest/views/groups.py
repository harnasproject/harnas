from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from guardian.shortcuts import assign_perm

from harnas.contest.models import Contest, GroupTaskDetails, Task
from harnas.contest.forms import GroupForm, TaskDetailsForm
from harnas.utils import permission_denied_message


@login_required
@require_POST
def new(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    if request.user.has_perm('manage_contest', contest):
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            group_name = contest.name + "_" + group_form.cleaned_data['name']
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                assign_perm('view_contest', group, contest)
                group.save()

                for task in Task.objects.filter(contest=contest_id):
                    GroupTaskDetails.objects.create(task=task,
                                                    group=group,
                                                    open=task.open,
                                                    deadline=task.deadline,
                                                    close=task.close)
                success_msg = 'New group %s for contest %s has been created.' % (group.name, contest.name)
                messages.add_message(request,
                                     messages.SUCCESS,
                                     success_msg
                                     )
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Group with that name already exists.')
    else:
        permission_denied_message(request)

    return HttpResponseRedirect(reverse('contest_details',
                                        args=[contest_id, 'groups']))


@login_required
@require_GET
def view(request, contest_id, group_id):
    contest = Contest.objects.get(pk=contest_id)
    if not request.user.has_perm('view_contest', contest):
        permission_denied_message(request)
        return HttpResponseRedirect('/')
    else:
        group = Group.objects.get(pk=group_id)

        return render(request, 'contest/group_details.html', {
            'contest': contest,
            'group': group,
            'tasks_details': GroupTaskDetails.objects.filter(group=group_id),
            'participants': group.user_set.all()
        })


@login_required
@require_http_methods(['POST', 'GET'])
def edit_task_details(request, contest_id, group_id, task_id):
    if not request.user.has_perm('manage_contest', Contest.objects.get(pk=contest_id)):
        permission_denied_message(request)
        return HttpResponseRedirect(reverse('contest_details', args=[contest_id]))
    else:
        if request.method == 'POST':
            form = TaskDetailsForm(request.POST)
            if form.is_valid():
                details = GroupTaskDetails.objects.get(group=group_id, task=task_id)
                details.open = form.cleaned_data['open']
                details.deadline = form.cleaned_data['deadline']
                details.close = form.cleaned_data['close']
                details.save()
                messages.add_message(request, messages.SUCCESS, "Timestamps have been updated.")
                return HttpResponseRedirect(reverse('contest_group_details', args=[contest_id, group_id]))
        else:
            details = GroupTaskDetails.objects.get(task=task_id, group=group_id)
            return render(request, 'contest/task_details_edit.html', {
                'contest_id': contest_id,
                'group_id': group_id,
                'task': Task.objects.get(pk=task_id),
                'form': TaskDetailsForm(instance=details),
            })


@login_required
def delete(request, contest_id, group_id):
    if not request.user.has_perm('manage_contest', Contest.objects.get(pk=contest_id)):
        permission_denied_message(request)
        return HttpResponseRedirect(reverse('contest_details', args=[contest_id, 'groups']))
    else:
        try:
            Group.objects.get(pk=group_id).delete()
            messages.add_message(request, messages.SUCCESS, "Group has been successfully deleted.")
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, "Group does not exists.")
        return HttpResponseRedirect(reverse('contest_details', args=[contest_id, 'groups']))

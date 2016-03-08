from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.decorators.http import require_POST
from guardian.shortcuts import assign_perm

from harnas.contest.models import Contest
from harnas.contest.forms import GroupForm


@login_required
@require_POST
def new(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    if request.user.has_perm('manage_contest', contest):
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            group, created = Group.objects.get_or_create(name=contest.name + "_" + group_form.cleaned_data['name'])
            if created:
                assign_perm('view_contest', group, contest)
                group.save()
                messages.add_message(request, messages.SUCCESS,
                                     'New group %s for contest %s has been created.' % (group.name, contest.name))
            else:
                messages.add_message(request, messages.ERROR, 'Group with that name already exists.')
    else:
        messages.add_message(request, messages.ERROR, 'You cannot do that.')

    return HttpResponseRedirect(reverse('contest_details', args=[contest_id, 'groups']))


@login_required
def edit(request, contest_id, group_id):
    return render(request, 'contest/group_edit.html', {
        'group': Group.objects.get(pk=group_id)
    })


@login_required
def delete(request, contest_id, group_id):
    if request.user.has_perm('manage_contest', Contest.objects.get(pk=contest_id)):
        try:
            Group.objects.get(pk=group_id).delete()
            messages.add_message(request, messages.SUCCESS, "Group has been successfully deleted.")
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, "Group does not exists.")
    else:
        messages.add_message(request, messages.ERROR, "You cannot do that.")

    return HttpResponseRedirect(reverse('contest_details', args=[contest_id, 'groups']))

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm

from harnas.contest.models import Contest
from harnas.contest.forms import GroupForm


def new(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
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

    return HttpResponseRedirect(reverse('contest_details', args=[contest_id]))

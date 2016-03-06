from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_safe
from guardian.shortcuts import assign_perm, get_users_with_perms, get_groups_with_perms
from harnas.contest.models import Contest
from harnas.contest.forms import ContestForm, NewsForm, GroupForm


@require_safe
def index(request):
    return render(request, 'contest/contest_index.html')


@require_safe
@login_required
def details(request, id):
    contest = Contest.objects.get(pk=id)
    if not request.user.has_perm('contest.view_contest', contest):
        raise PermissionDenied
    contest_form = ContestForm(instance=contest)
    groups = get_groups_with_perms(contest, attach_perms=True)
    groups = [k for k, v in groups.items() if 'view_contest' in v]
    group_form = GroupForm()
    news = contest.news_set.all().order_by('-created_at')
    news_form = NewsForm()
    if request.user.has_perm('contest.manage_contest', contest):
        participants = get_users_with_perms(contest, attach_perms=True)
        participants = [k for k, v in participants.items()
                        if 'participate_in_contest' in v]
    else:
        participants = []
    return render(request, 'contest/contest_details.html',
                  { 'contest': contest,
                    'contest_form': contest_form,
                    'groups': groups,
                    'group_form': group_form,
                    'participants': participants,
                    'news_form': news_form,
                    'news': news })


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, id=None):
    if id:
        contest = Contest.objects.get(pk=id)
        form_post = reverse('contest_edit', args=[id])
        if not request.user.has_perm('contest.manage_contest', contest):
            raise PermissionDenied
    else:
        contest = Contest()
        form_post = reverse('contest_new')
        if not request.user.has_perm('contest.add_contest'):
            raise PermissionDenied
    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
    else:
        form = ContestForm(instance=contest)
    if form.is_valid():
        new_contest = form.save(commit=False)
        new_contest.slug = slugify(new_contest.name)
        if id is None:
            new_contest.creator_id = request.user.pk
        new_contest.save()
        assign_perm('contest.manage_contest', request.user, new_contest)
        assign_perm('contest.view_contest', request.user, new_contest)
        cache_key = make_template_fragment_key('contest_description',
                                               [new_contest.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('contest_details',
                                            args=[new_contest.pk]))
    return render(request, 'contest/contest_new.html',
                  { 'form': form,
                    'form_post': form_post })

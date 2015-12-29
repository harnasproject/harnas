from django.shortcuts import render
from .models import Contest, ContestForm
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

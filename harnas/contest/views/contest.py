from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_safe
from guardian.decorators import permission_required
from guardian.shortcuts import assign_perm
from harnas.contest.models import Contest, ContestForm, NewsForm, News


@require_safe
def index(request):
    return render(request, 'contest/contest_index.html')


@require_safe
@permission_required('contest.view', (Contest, 'id', 'id'))
def details(request, id):
    contest = Contest.objects.get(pk=id)
    form = ContestForm(instance=contest)
    news_form = NewsForm()
    return render(request, 'contest/contest_details.html', { 'contest': contest, 'form': form, 'news_form' :news_form })


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, id=None):
    if id:
        contest = Contest.objects.get(pk=id)
        form_post = reverse('contest_edit', args=[id])
        if not request.user.has_perm('contest.manage',contest):
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
        assign_perm('contest.manage', request.user, new_contest)
        assign_perm('contest.view', request.user, new_contest)
        cache_key = make_template_fragment_key('contest_description', [new_contest.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('contest_details', args=[new_contest.pk]))
    return render(request, 'contest/contest_new.html', { 'form': form, 'form_post': form_post })

def add_news(request, id):
    contest = get_object_or_404(Contest, pk=id)
    contest.news_set.create(title=request.POST['title'],
                            description=request.POST['description'],
                            author=request.user,
                            contest=contest
                            )
    return HttpResponseRedirect(reverse('contest_details', args=[id]))

def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    contest = news.contest
    news.delete()
    return HttpResponseRedirect(reverse('contest_details', args=[contest.pk]))
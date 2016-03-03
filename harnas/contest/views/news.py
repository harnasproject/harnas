from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_safe
from guardian.decorators import permission_required
from harnas.contest.models import Contest, News
from harnas.contest.forms import NewsForm


@require_http_methods(['GET', 'POST'])
def new(request, id):
    form = NewsForm(request.POST)
    if form.is_valid():
        contest = get_object_or_404(Contest, pk=id)
        contest.news_set.create(
            title=form.data['title'],
            description=form.data['description'],
            contest=contest,
            author=request.user
            )
    return HttpResponseRedirect(reverse('contest_details', args=[id]))


@require_safe
def delete(request, id):
    news = get_object_or_404(News, pk=id)
    contest = news.contest
    news.delete()
    return HttpResponseRedirect(reverse('contest_details', args=[contest.pk]))


@require_http_methods(['GET', 'POST'])
def edit(request, id):
    news = get_object_or_404(News, pk=id)
    contest_pk = news.contest.pk
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('contest_details', args=[contest_pk]))
    form = NewsForm(instance=news)
    return render(request, 'contest/news_edit.html', {'form': form})

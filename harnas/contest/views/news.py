from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_safe
from guardian.decorators import permission_required
from harnas.contest.models import Contest, NewsForm, News

def news_new(request, id):
    contest = get_object_or_404(Contest, pk=id)
    contest.news_set.create(title=request.POST['title'],
                            description=request.POST['description'],
                            author=request.user,
                            contest=contest
                            )
    return HttpResponseRedirect(reverse('contest_details', args=[id]))

def news_delete(request, id):
    news = get_object_or_404(News, pk=id)
    contest = news.contest
    news.delete()
    return HttpResponseRedirect(reverse('contest_details', args=[contest.pk]))

def news_edit(request, id):
    news = get_object_or_404(News, pk=id)
    contest_pk = news.contest.pk
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        form.save(commit=True)
        return HttpResponseRedirect(reverse('contest_details', args=[contest_pk]))
    else:
        form = NewsForm(instance=news)
        return render(request, 'contest/news_edit.html', {'form': form})
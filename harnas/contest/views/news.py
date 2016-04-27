from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from harnas.contest.forms import NewsForm
from harnas.contest.models import Contest, News


@require_http_methods(['GET', 'POST'])
def new(request, contest_id):
    if not request.user.has_perm('manage_contest',
                                 Contest.objects.get(pk=contest_id)):
        raise PermissionDenied
        return HttpResponseRedirect(request,
                                    reverse('contest_details',
                                            args=[contest_id]))
    else:
        form = NewsForm(request.POST)
        if form.is_valid():
            contest = Contest.objects.get(pk=contest_id)
            contest.news_set.create(
                title=form.data['title'],
                description=form.data['description'],
                contest=contest,
                author=request.user)
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "New news has been created.")
        return HttpResponseRedirect(reverse('contest_details',
                                            args=[contest_id]))


@require_safe
def delete(request, contest_id, news_id):
    if not request.user.has_perm('manage_contest',
                                 Contest.objects.get(pk=contest_id)):
        raise PermissionDenied
        return HttpResponseRedirect(request,
                                    reverse('contest_details',
                                            args=[contest_id]))
    else:
        try:
            news = News.objects.get(pk=news_id)
            news.delete()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "News deleted successfully.")
        except ObjectDoesNotExist:
            raise PermissionDenied
        return HttpResponseRedirect(reverse('contest_details',
                                            args=[contest_id]))


@require_http_methods(['POST', 'GET'])
def edit(request, contest_id, news_id):
    if not request.user.has_perm('manage_contest',
                                 Contest.objects.get(pk=contest_id)):
        raise PermissionDenied
        return HttpResponseRedirect(request,
                                    reverse('contest_details',
                                            args=[contest_id]))
    else:
        try:
            news = News.objects.get(pk=news_id)
            if request.method == 'POST':
                form = NewsForm(request.POST, instance=news)
                if form.is_valid():
                    form.save(commit=True)
            else:
                return render(request, 'contest/news_edit.html', {
                    'form': NewsForm(instance=news),
                })
        except ObjectDoesNotExist:
            raise PermissionDenied
        return HttpResponseRedirect(reverse('contest_details',
                                            args=[contest_id]))

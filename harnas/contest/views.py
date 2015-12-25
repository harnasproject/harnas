from django.shortcuts import render
from .models import Contest
from guardian.decorators import permission_required
from django.forms import ModelForm
from django.views.decorators.http import require_safe, require_http_methods
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

@require_safe
def index(request):
    return render(request, 'contest/index.html')

@require_safe
@permission_required('contest.view')
def details(request, id):
    contest = Contest.objects.get(pk=id)
    return render(request, 'contest/details.html', { 'contest': contest })

class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'slug', 'description']

@require_http_methods(['GET', 'POST'])
@permission_required('contest.add_contest')
def new(request):
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            new_contest = form.save()
            return HttpResponseRedirect(reverse('contest_details', args=(new_contest.pk,)))
    else:
        form = ContestForm()
    return render(request, 'contest/new.html', { 'form': form })
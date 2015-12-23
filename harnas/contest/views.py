from django.shortcuts import render
from .models import Contest
from guardian.decorators import permission_required

def index(request):
    return render(request, 'contest/index.html')

@permission_required('contest.view')
def details(request, id):
    contest = Contest.objects.get(pk=id)
    return render(request, 'contest/details.html', { 'contest': contest })

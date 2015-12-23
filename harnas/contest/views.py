from django.shortcuts import render
from .models import Contest

def index(request):
    return render(request, 'contest/index.html')

def details(request, id):
    contest = Contest.objects.get(pk=id)
    return render(request, 'contest/details.html', { 'contest': contest })

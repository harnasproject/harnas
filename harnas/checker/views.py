from django.shortcuts import render
from heraclient import get_cluster
from django.conf import settings
from django.views.decorators.http import require_safe

auth = (settings.HERA_USER, settings.HERA_API_KEY)

@require_safe
def status(request):
    nodes = get_cluster(auth)
    return render(request, 'checker/status.html', dict(nodes = nodes))
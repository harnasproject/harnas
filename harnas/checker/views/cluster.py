from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_safe
from harnas.checker.heraclient import get_cluster


@require_safe
def status(request):
    nodes = get_cluster(settings.HERA_AUTH)
    return render(request, 'checker/status.html', {'nodes': nodes})

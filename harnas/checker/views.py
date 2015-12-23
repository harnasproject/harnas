from django.shortcuts import render
import os
from heraclient import get_cluster
from django.conf import settings
import json

auth = (settings.HERA_USER, settings.HERA_API_KEY)

def status(request):
    nodes = get_cluster(auth)
    return render(request, 'checker/status.html', dict(nodes = nodes))

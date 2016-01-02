from django.shortcuts import render
from django.views.decorators.http import require_safe
from harnas.checker.utils import get_templates_list


@require_safe
def index(request):
    templates = [ (template.id, template.name)
                   for template in get_templates_list() ]
    return render(request,
                  'checker/template_index.html',
                  {'templates': templates})

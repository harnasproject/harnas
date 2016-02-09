from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_safe
from guardian.shortcuts import get_objects_for_user
from harnas.checker.utils import get_templates_list


@require_safe
@login_required
def index(request):
    has_editable_test_envs = \
        get_objects_for_user(request.user,
                             'checker.edit_test_environment').count() > 0
    if (
        not request.user.has_perm('checker.add_test_environment') and
        not has_editable_test_envs
    ):
        raise PermissionDenied
    templates = [ (template.id, template.name)
                   for template in get_templates_list() ]
    return render(request,
                  'checker/template_index.html',
                  { 'templates': templates })

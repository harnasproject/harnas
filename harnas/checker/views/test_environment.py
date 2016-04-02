from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from guardian.shortcuts import assign_perm
from harnas.checker.models import TestEnvironment
from harnas.checker.forms import TestEnvironmentForm


@require_safe
@login_required
def index(request):
    test_envs = TestEnvironment.objects.all()
    return render(request,
                  'checker/test_environment_index.html',
                  {'test_envs': test_envs})


@require_safe
@login_required
def details(request, id):
    test_env = TestEnvironment.objects.get(pk=id)
    if not request.user.has_perm('checker.view_test_environment', test_env):
        raise PermissionDenied
    return render(request, 'checker/test_environment_details.html',
                  {'test_env': test_env})


@require_http_methods(['GET', 'POST'])
@login_required
def edit(request, id=None):
    if id:
        test_env = TestEnvironment.objects.get(pk=id)
        form_post = reverse('test_environment_edit', args=[id])
        if not request.user.has_perm('checker.edit_test_environment',
                                     test_env):
            raise PermissionDenied
    else:
        test_env = TestEnvironment(maintainer=request.user)
        form_post = reverse('test_environment_new')
        if not request.user.has_perm('checker.add_test_environment'):
            raise PermissionDenied
    if request.method == "POST":
        form = TestEnvironmentForm(request.POST, instance=test_env)
    else:
        form = TestEnvironmentForm(instance=test_env)
    if form.is_valid():
        new_test_env = form.save(commit=False)
        # I suppose there is a nicer way to do this, but it works.
        new_test_env.template_name = form.cleaned_data['template_name']
        new_test_env.save()
        assign_perm('checker.view_test_environment',
                    request.user,
                    new_test_env)
        assign_perm('checker.edit_test_environment',
                    request.user,
                    new_test_env)
        cache_key = make_template_fragment_key('test_environment_description',
                                               [new_test_env.pk])
        cache.delete(cache_key)
        return HttpResponseRedirect(reverse('test_environment_details',
                                            args=[new_test_env.pk]))
    return render(request, 'checker/test_environment_new.html', {
                  'form': form,
                  'form_post': form_post})

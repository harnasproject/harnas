from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_safe
from harnas.checker.models import TestEnvironment, TestEnvironmentForm


@require_safe
def index(request):
    test_envs = TestEnvironment.objects.all()
    return render(request,
                  'checker/test_environment_index.html',
                  {'test_envs': test_envs})


@require_safe
def details(request, id):
    test_env = TestEnvironment.objects.get(pk=id)
    return render(request, 'checker/test_environment_details.html', {'test_env': test_env})


@require_http_methods(['GET', 'POST'])
def edit(request, id=None):
    if id:
        test_env = TestEnvironment.objects.get(pk=id)
        form_post = reverse('test_environment_edit', args=[id])
    else:
        # Will crush if user is anonymous, but this shouldn't happen
        test_env = TestEnvironment(maintainer=request.user)
        form_post = reverse('test_environment_new')
    if request.method == "POST":
        form = TestEnvironmentForm(request.POST, instance=test_env)
    else:
        form = TestEnvironmentForm(instance=test_env)
    if form.is_valid():
        new_test_env = form.save(commit=False)
        # I suppose there is a nicer way to do this, but it works.
        new_test_env.template_name = form.cleaned_data['template_name']
        new_test_env.save()
        return HttpResponseRedirect(reverse('test_environment_details', args=[new_test_env.pk]))
    return render(request, 'checker/test_environment_new.html', {'form': form, 'form_post': form_post})

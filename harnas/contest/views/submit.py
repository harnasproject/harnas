from django.views.decorators.http import require_http_methods, require_safe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from harnas.checker.models import Submit


@login_required
@require_safe
def details(request, id):
    submit = Submit.objects.get(pk=id)
    solution = bytes(submit.solution).decode("utf-8")
    return render(request, 'contest/submit_details.html', {
        'submit': submit,
        'solution': solution,
    })

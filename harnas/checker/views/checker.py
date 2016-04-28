from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from harnas.checker.models import Submit
from harnas.contest.models import TestCase


@require_POST
@csrf_exempt
def check(request, submit_id):
    submit = Submit.objects.get(pk=submit_id)
    webhook_secret = request.POST.get('secret')
    if _is_webhook_secret_valid(submit, webhook_secret):
        response = JsonResponse({'status': 'ok'}, status=200)
    else:
        response = JsonResponse({'status': 'Forbidden. Bad webhook secret.'},
                                status=403)
        submit.change_status(TestCase.QUEUED)
    return response


def _is_webhook_secret_valid(submit, webhook_secret):
    return submit.webhook_secret == webhook_secret

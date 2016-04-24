from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@require_POST
@csrf_exempt
def check(request):
    response = JsonResponse({'status': 'ok'}, status=200)
    return response

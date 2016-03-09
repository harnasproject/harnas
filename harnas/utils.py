from django.contrib import messages
from django.http import HttpResponseRedirect


def permission_denied_message(request):
    messages.add_message(request, messages.ERROR, "You cannot do that.")

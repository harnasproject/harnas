from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_GET

from harnas.userprofile.forms import UserFieldsForm, UserProfileEditForm


@require_GET
def show(request, user_id):
    try:
        return render(request, 'profile.html', {
            'user': User.objects.get(id=user_id)
        })
    except User.DoesNotExist:
        raise Http404


@login_required
def edit(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserFieldsForm(request.POST or None, instance=user)
        if user_form.is_valid():
            user_form.save()

        profile_form = UserProfileEditForm(
              request.POST or None,
              instance=user.userprofile
        )
        if profile_form.is_valid():
            profile_form.save()

        return HttpResponseRedirect('/accounts/' + str(user.id))
    else:
        return render_to_response(
              'edit_profile.html',
              {
                  'user': request.user,
                  'user_form': UserFieldsForm(instance=user),
                  'profile_form': UserProfileEditForm(
                        instance=user.userprofile
                  )
              },
              context_instance=RequestContext(request)
        )

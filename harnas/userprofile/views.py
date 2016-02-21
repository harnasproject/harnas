from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

from harnas.userprofile.forms import UserFieldsForm, UserProfileEditForm


@require_safe
def show(request, user_id):
    """
    :return: profile of a user specified by user_id.
    """
    try:
        user = User.objects.get(id=user_id)
        today = date.today()
        born = user.userprofile.date_of_birth
        return render(request, 'profile.html', {
            'user': user,
            'profile': user.userprofile,
            'age': today.year - born.year - (
                (today.month, today.day) < (born.month, born.day))
        })
    except User.DoesNotExist:
        raise Http404


@login_required
def edit(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserFieldsForm(request.POST or None, instance=user)
        profile_form = UserProfileEditForm(
              request.POST or None,
              instance=user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/accounts/' + str(user.id))
        else:
            return render_to_response(
                  'edit_profile.html',
                  {
                      'user': user,
                      'user_form': user_form,
                      'profile_form': profile_form
                  },
                  context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
              'edit_profile.html',
              {
                  'user': user,
                  'user_form': UserFieldsForm(instance=user),
                  'profile_form': UserProfileEditForm(
                        instance=user.userprofile
                  )
              },
              context_instance=RequestContext(request)
        )

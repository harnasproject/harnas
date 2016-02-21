from registration.backends.default import views


class RegistrationView(views.RegistrationView):
    """
    Overrode Registration view for handling initial user profile data saving
    during registration.
    """

    def register(self, request, form):
        user = super(RegistrationView, self).register(request, form)

        user.userprofile.date_of_birth = form.cleaned_data['date_of_birth']
        user.userprofile.organization = form.cleaned_data['organization']
        user.userprofile.save()

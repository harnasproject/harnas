from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from harnas.userprofile.models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class ExtendedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

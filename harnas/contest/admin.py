from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from harnas.contest import models


class ContestAdmin(GuardedModelAdmin):
    list_display = ('slug', 'name')

admin.site.register(models.Contest, ContestAdmin)

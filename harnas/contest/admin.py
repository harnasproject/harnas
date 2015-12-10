from django.contrib import admin
from harnas.contest import models
from guardian.admin import GuardedModelAdmin

class ContestAdmin(GuardedModelAdmin):
    list_display = ('slug', 'title')

admin.site.register(models.Contest, ContestAdmin)

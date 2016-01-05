from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from harnas.contest import models


class ContestAdmin(GuardedModelAdmin):
    list_display = ('slug', 'name')

admin.site.register(models.Contest, ContestAdmin)


class TaskAdmin(GuardedModelAdmin):
    list_display = ('short_name', 'name', 'author')

admin.site.register(models.Task, TaskAdmin)


class NewsAdmin(GuardedModelAdmin):
    list_display = ('title', 'contest', 'author')

admin.site.register(models.News, NewsAdmin)

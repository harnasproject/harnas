from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from harnas.checker import models


class TestEnvironmentAdmin(GuardedModelAdmin):
    list_display = ('template_name', 'summary')

admin.site.register(models.TestEnvironment, TestEnvironmentAdmin)

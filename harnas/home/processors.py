from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.models import User
from harnas.contest.models import Task


def task_manager_permissions(request):
    has_editable_tasks = get_objects_for_user(request.user,
                                              'contest.edit_task').count() > 0
    can_add_task = request.user.has_perm('contest.add_task')
    can_add_test_environment = request.user.has_perm('checker.add_test_environment')
    can_view_task_manager = (has_editable_tasks or
                             can_add_task or
                             can_add_test_environment)
    return { 'can_view_task_manager': can_view_task_manager,
             'can_add_task': can_add_task,
             'can_add_test_environment': can_add_test_environment }

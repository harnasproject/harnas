from guardian.shortcuts import get_objects_for_user
from harnas.contest import models

def contests(request):
    return {'contests': get_objects_for_user(request.user, 'contest.view')}

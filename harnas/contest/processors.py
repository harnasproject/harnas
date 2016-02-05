from guardian.shortcuts import get_objects_for_user


def contests(request):
    return {'contests':
                get_objects_for_user(request.user, 'contest.view_contest')
                    .order_by('-created_at')}

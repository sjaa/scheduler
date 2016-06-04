from .models import UserPermission


# assume 'Group' doesn't change during session
all_groups = Group.objects.all()

def get_coordinator_groups(user):
    # get groups for which 'user' is a coordinator
    if user.is_staff:
        groups = all_groups
    else:
        user_perm = UserPermission.objects.get(pk=user.pk)
        groups    = user_perm.coordinator
    return groups


from .models import UserPermission


# assume 'Group' doesn't change during session
all_groups = Group.objects.all()

'''
class user_perms():
    def __init__(self, groups, coordinator):
        self.groups      = groups
        self.coordinator = coordinator
    def in_group(self, user, group):
        user_perm = UserPermission.objects.get(pk=user.pk)
        in_group = group in user_perm.groups
        return in_group
    def is_coordinator(self, user, group):
        user_perm = UserPermission.objects.get(pk=user.pk)
        in_group = group in user_perm.groups
        return in_group
'''

class user_perms():
    def __init__(self, user):
        self.user_perm   = UserPermission.objects.get(pk=user.pk)
        self.groups      = user_perm.groups.all()
        self.coordinator = user_perm.coordinator.all()
    def group(self, group):
        in_group = group in self.groups
        return in_group
    def coordinator(self, group):
        in_group = group in self.coordinator
        return in_group

'''
def get_coordinator_groups(user):
    # get groups for which 'user' is a coordinator
    if user.is_staff:
        groups = all_groups
    else:
        user_perm = UserPermission.objects.get(pk=user.pk)
        up = user_perms(groups     =user_perm.groups,
                        coordinator=user_perm.coordinator)
    return up
'''

'''
Task
    task type - add auto fill of coordinator
'''

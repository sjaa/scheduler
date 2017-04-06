import pdb
from django.contrib.auth.models import Group


def get_perm_groups():
    groups = Group.objects.all()
    perm_groups = []
    for group in groups:
        name = group.name
        coordinators = group.perm_coordinator.all()
        members      = group.perm_group.all()
        coord = []
        for up in coordinators:
            coord.append(up.user.get_full_name())
        mem   = []
        for up in members:
            mem.append(up.user.get_full_name())
        perm_groups.append((name, coord, mem))
    return perm_groups


def report_groups():
    perm_groups = get_perm_groups()
    for group in perm_groups:
        len_coord   = len(group[1])
        len_mem     = len(group[2])
        group_name  = group[0]
        coordinator = group[1][0] if len_coord else '--none--'
        member      = group[2][0] if len_mem   else '--none--'
        print('{:30}  {:15}  {:15}'.format('', 'coordinator ({:1})'.format(len_coord), 'member ({:2})'.format(len_mem )))
        print('{:30}  {:15}  {:15}'.format(group_name, coordinator, member))
#       print('hi')
        group_name  = ''
        pdb.set_trace()
        for i in range(1, max(len_coord, len_mem)):
#           print(i)
#           print(group[1])
#           print(group[2])
            coordinator = group[1][i] if len_coord else ''
            member      = group[2][i] if len_mem   else ''
            print('{:30}  {:15}  {:15}'.format(group_name, coordinator, member))
        print('')

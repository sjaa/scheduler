

def get_user_groups(user)
    grp = event.group
    grp_lead = Groups.objects.filter(name=grp.name + '_lead')

def verify_perm(user, event):
    grp = event.group
    grp_lead = Groups.objects.filter(name=grp.name + '_lead')
    perm = user.grp or user.grp_lead
    return perm


def get_editable_tasks(user):
    groups_for_user  = Tas.group
    groups_for_user += Groups.objects.filter(name=grp.name + '_lead')
    groups_for_user += Groups.objects.filter(name=grp.name + '_lead')

    groups_for_user += user.groups.all()

    tasks = Tasks.objects.filter(group__in=groups_for_user)




'''
Need code to add/delete users from groups.
If user is lead
    can add/delete to/from lead group
        add - also add to group
        can't delete self if there are no other leads in group
    can add/delete to/from group
        can't delete self if there are no other leads in group
'''

import pdb
import datetime

from   sched_core.const           import FMT_HMP
from   sched_core.config          import local_time
from   sched_ev.cal_ephemeris     import calc_date_ephem
from   membership.models          import User
from   .event_owner               import get_event_owner
from   .config                    import descr_month_dict


def gen_label_time_offset(event, var):
    # e.g.: start+15m (15 min after start), end-30m (30 min before end)
    #       var   = 'start+15m'
    #       label = 'start'
    '''
    If 'var' looks like some_var+15m, return 
    '''
    # find '+' or '-'
    if var[0:5]=='start' or var[0:3]=='end':
        i = var.find('+')
        if i == -1:
            i = var.find('-')
        if i == -1:
            # no '+', '-'
            # do stuff
            label = var
        else:
            label = var[0:i]
    elif var == 'sunset':
        sunset, moon = calc_date_ephem(event.date_time, event.location)
        t = sunset[0]
        return t.lstrip('0')
    elif var == 'open':
        t = local_time_str(event.date_time-event.time_setup, FMT_HMP)
        return t.lstrip('0')
    elif var == 'close':
        t = local_time_str(event.date_time+event.time_length+event.time_teardown, FMT_HMP)
        return t.lstrip('0')
    else:
        # var not time label
        return None
    if len(var)>=i+3 and var[-1]=='m' or var=='start' or var=='end':
        try:
            if var=='start' or var=='end':
                delta = 0  # no offset
            else:
                delta = int(var[i:-1]) # minutes
            t = local_time(event.date_time) + datetime.timedelta(minutes=delta)
            if label == 'start':
                # calculate start time + offset
                subst_str = t.strftime('%I:%M %p').lstrip('0')
            elif label == 'end':
                # calculate end time
                t = t + event.time_length
                subst_str = t.strftime('%I:%M %p').lstrip('0')
            else:
                subst_str = 'BAD LABEL:"' + var + '"'
        except:
            subst_str = 'BAD LABEL:"' + var + '"'
    else:
        subst_str = 'BAD LABEL:"' + var + '"'
    return subst_str

def add_time_labels(mydict, event, description):
    d = description
    idx = 0
    while d:
        left = d.find('{', idx)
        if left == -1:
            # no '{' found
            break
        else:
            left += 1
            right = d.find('}', left)
            if right == -1:
                # no '}' found
                break
            else:
                # extract label
                label = d[left:right]
                # generate label time offset if applicable
                subst_str = gen_label_time_offset(event, label)
                if subst_str:
                    # add label to mydict
                    mydict[label] = subst_str
        idx = right + 1
    return mydict

def parse_labels(description):
    d = description
    labels = []
    idx = 0
    # find instances of {} in 'description'
    while d:
        left = d.find('{', idx)
        if left == -1:
            # no '{' found
            break
        else:
            left += 1
            right = d.find('}', left)
            if right == -1:
                # no '}' found
                break
            else:
                # extract label
                label = d[left:right]
                labels.append(label)
        idx = right + 1
    return labels

def gen_description(announce):
    description = announce.description()
    ev = announce.event
    month = ev.date_time.month
    owner = get_event_owner(ev)
    # build substitution dictionary
    # define default labels
    event_label_dict = {
            'lead_title'      : announce.lead_title  ,
            'lead'            : owner.get_full_name(),
            'url'             : ev.url}
    try:
        # extract time labels to 'event_label_dict'
        add_time_labels(event_label_dict, ev, description)
        # add labels in 'descr_month_dict'
        labels = parse_labels(description)
        for label in labels:
            if label not in event_label_dict and label in descr_month_dict:
                event_label_dict[label] = descr_month_dict[label][month]
    except KeyError as ex:
        new_description = 'Bad label:"{}"'.format(ex)
    # do label substitution
    try:
        new_description = description.format(**event_label_dict)
    except KeyError:
        # bad label -> replace description with error message
        labels = parse_labels(description)
        new_description = 'Undefined label(s) found'
        for l in labels:
            if not l in description:
                new_description += 'label "{}" not found<br>'.format(l)
    except Exception as ex:
        new_description = 'gen_description - exception: {}'.format(type(ex))
    return new_description

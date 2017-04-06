
import pdb
import datetime
from django.contrib.auth.models import User

from   sched_announce.event_owner import get_event_owner
from   sched_announce.config      import objects_month_talk, objects_month_observe


def gen_label_time_offset(event, var):
#def gen_label_time_offset(var):
    # e.g.: start+15m (15 min after start), end-30m (30 min before end)
    #       var   = 'start+15m'
    #       label = 'start'
    '''
    If 'var' looks like some_var+15m, return 
    '''
    # find '+' or '-'
#   pdb.set_trace()
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
    else:
        # var not time label
        return None
    if len(var)>=i+3 and var[-1]=='m' or var=='start' or var=='end':
        try:
            if var=='start' or var=='end':
                delta = 0  # no offset
            else:
                delta = int(var[i:-1]) # minutes
            t = event.date_time + datetime.timedelta(minutes=delta)
            #t = datetime.datetime(2017, 4, 10, 20, 17)
            t = t + datetime.timedelta(minutes=delta)
            if label == 'start':
                # calculate start time + offset
                subst_str = t.strftime('%I:%M %p').lstrip('0')
            elif label == 'end':
                # calculate end time + offset
                t = t + event.time_length
                #t = t + datetime.timedelta(minutes=30)
                subst_str = t.strftime('%I:%M %p').lstrip('0')
            else:
                subst_str = 'BAD LABEL:"' + var + '"'
        except:
            subst_str = 'BAD LABEL:"' + var + '"'
    else:
        subst_str = 'BAD LABEL:"' + var + '"'
    return subst_str

#def parse_time_labels(event, description):
def parse_time_labels(event, description):
    d = description
    mydict = {}
    idx = 0
#   pdb.set_trace()
    while d:
        left = d.find('{', idx)
        if left == -1:
            # no '{' found
            break
        else:
#           d = d[left+1:]
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
#   pdb.set_trace()
    return mydict

#def parse_time_labels(event, description):
def parse_labels(description):
    d = description
    labels = []
    idx = 0
    while d:
        left = d.find('{', idx)
        if left == -1:
            # no '{' found
            break
        else:
#           d = d[left+1:]
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
#       d = d[right+1:]
#   pdb.set_trace()
    return labels

def gen_description(announce):
    description = announce.description()
    ev = announce.event
    month = ev.date_time.month
    owner = get_event_owner(ev)
    # build generic substitution dictionary
    try:
        event_label_dict = {
                'lead_title'      : announce.lead_title  ,
                'lead'            : owner.get_full_name(),
                'talk_objects'    : objects_month_talk   [month],
                'observe_objects' : objects_month_observe[month],
                'url'             : ev.url}
    except KeyError as ex:
        new_description = 'Bad label:"{}"'.format(ex)
    # apply generic substitution dictionary to description
    try:
        new_description = description.format(**event_label_dict)
    except KeyError:
        # bad label -> replace description with error message
        labels = parse_labels(description)
        new_description = 'Undefined label(s) found<br>'
        for l in labels:
            if not l in description:
                new_description += 'label "{}" not found<br>'.format(l)
    except Exception as ex:
        new_description = 'gen_description - exception: {}'.format(type(ex))
    # build time substitution dictionary
    time_dict = parse_time_labels(ev, description)
    new_description = new_description.format(**time_dict) \
                        if time_dict else new_description
    return new_description

'''
description = 'please arrive by {start-15m}. gates close at {end+15m}'
dd = 'please arrive by {start-15x}. gates close at {tend+15m}'
de = 'please arrive by {start}. gates close at {tend+15m}'

md = parse_time_labels(description)
new_description = description.format(**md) if md else description

labels = parse_labels(description)
labels.append('foo')
for l in labels:
    if l in description:
        print('found {} in description'.format(l))
    else:
        print('found NOT {} in description'.format(l))
'''

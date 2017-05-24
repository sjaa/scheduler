import pdb
import datetime
from   django.shortcuts            import render, get_object_or_404

from sched_core.config import local_date_now
from .forms            import TestForm
from membership.tester import tester

def test (request):
#   pdb.set_trace()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            date_start   = form.cleaned_data['date_start'  ]
            date_end     = form.cleaned_data['date_end'    ]
            date_current = form.cleaned_data['date_current']
            app          = form.cleaned_data['app'         ]
            test_modes   = form.cleaned_data['test_modes'  ]
            advance_mode = form.cleaned_data['advance_mode']
#           return render(request, 'test.html', {'form': user})
            # do something
#           pdb.set_trace()
            if date_current <= date_end:
                end_of_test = False
                if app == 'mem':
                    date_current = tester(request.user.username[:15],
                                          date_end, date_current,
                                          test_modes, advance_mode)
                    if date_current > date_end:
                        end_of_test = True
                    form = TestForm(initial={'date_start'  : date_start,
                                             'date_end'    : date_end,
                                             'date_current': date_current,
                                             'app'         : app,
                                             'test_modes'  : test_modes,
                                             'advance_mode': advance_mode})
            else:
                end_of_test = True
            return render(request, 'test.html', {'form'       : form,
                                                 'end_of_test': end_of_test})
        else:
            return render(request, 'test.html', {'form': form})
    else:
        today = datetime.date.today()
        form = TestForm(initial={'date_start'  : today,
                                 'date_end'    : today,
                                 'date_current': today,
                                 'app'         : 'mem',
                                 'advance_mode': '1day'})
        return render(request, 'test.html', {'form': form})


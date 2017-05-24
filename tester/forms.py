from django import forms

from sched_core.test       import TestModes
 

L_TEST_MODES = []
#L_TEST_MODES = [(TestModes.Fake_Save       .value, TestModes.Fake_Save       .value),
#                (TestModes.Email_To_Console.value, TestModes.Email_To_Console.value),
#                (TestModes.Email_To_Tester .value, '')]
for item in TestModes:
    L_TEST_MODES.append((item.value, item.value))

L_APPS = (
        ('mem', 'membership'),
        ('ann', 'announcements')
)

L_ADVANCE = (
        ('1day', '1 day'),
        ('next', 'next day with tasks'),
        ('all' , 'run to end date')
)


class TestForm(forms.Form):
    date_start   = forms.DateField(label='start date'  )
    date_end     = forms.DateField(label='end date'    )
    # TODO: hidden
    date_current = forms.DateField(label='current date')
    app = forms.ChoiceField(widget=forms.RadioSelect,
                            choices=L_APPS)
    test_modes_list = []
    for mode in TestModes:
        test_modes_list.append(mode.value)
#       print('test mode: {}'.format(mode))
    test_modes   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             required=False,
                                             initial=test_modes_list,
                                             choices=L_TEST_MODES)
#   advance_mode = forms.ChoiceField(choices=L_ADVANCE)
    advance_mode = forms.ChoiceField(widget=forms.RadioSelect,
                                     choices=L_ADVANCE)

'''
    def clean_date_current(self):
    data = self.cleaned_data['date_current']
    # do some stuff
    return data
'''

'''
x           date_start   = form.cleaned_data['date_start'  ]
x           date_end     = form.cleaned_data['date_end'    ]
x           date_current = form.cleaned_data['date_current']
x           app          = form.cleaned_data['app'         ]
x           test_modes   = form.cleaned_data['test_modes'  ]
x           advance_mode = form.cleaned_data['advance_mode']
            return render(request, 'test.html', {'form': user})
'''

'''

class TestForm(forms.Form):
    today = datetime.datetime.today()
    date_start   = forms.DateField(label='start date'   , initial=today)
    date_end     = forms.DateField(label='end date'     , initial=today)
    # TODO: hidden
    date_current = forms.DateField(label='current date' , initial=today)
    test_modes   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=L_TEST_MODES)
    app = forms.ChoiceField(choices=L_APPS)

from sched_core.lib import set_current_date
    set_current_date(date_current)

    while current_date <= date_end:
        # membership
        if APPS.membership in apps_to_test:
            ran_job = cron_job_membership()
            if step_day or step_next_job and ran_job:
                break
        # announce
        inc_current_date()

'''

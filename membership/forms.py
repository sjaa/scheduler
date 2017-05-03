from django            import forms
from django.forms      import formset_factory
 
from sched_core.config import current_year, local_date_now
from sched_ev  .models import L_MONTH

 
L_report_type = (
        ('summary' , 'Report - summary'),
        ('details' , 'Report - details'),
#       ('active'  , 'active'          ),
#       ('expiring', 'expiring'        ),
#       ('expired' , 'expired'         )
)

class ReportSearchForm(forms.Form):
    start_year  = forms.IntegerField(label='Starting year' , initial=current_year)
    start_month = forms.ChoiceField (label='Starting month', choices=L_MONTH, initial=1)
    start_day   = forms.IntegerField(label='Starting day'  , initial=1)
    end_year    = forms.IntegerField(label='Ending year'   , initial=current_year)
    end_month   = forms.ChoiceField (label='Ending month'  , choices=L_MONTH, initial=12)
    end_day     = forms.IntegerField(label='Ending day'    , initial=1)
    report_type = forms.ChoiceField (                        choices=L_report_type)
#   report_type =     form.cleaned_data['report_type']


class VerifyForm_Orion(forms.Form):
    first_name = forms.CharField(max_length=3)
    last_name  = forms.CharField(max_length=20)


class VerifyForm_Membership(forms.Form):
    email = forms.EmailField(max_length=40)

class RenewForm(forms.Form):
    term_start = forms.DateField()
    term_end   = forms.DateField()
    first_name = forms.CharField(max_length=20, widget=forms.HiddenInput())
    last_name  = forms.CharField(max_length=20, widget=forms.HiddenInput())
    email      = forms.CharField(max_length=40, widget=forms.HiddenInput())
    id         = forms.IntegerField(widget=forms.HiddenInput())

'''
class RenewForm(forms.formset_factory):
    first_name = forms.CharField(max_length=3)
    last_name  = forms.CharField(max_length=20)



    RenewalFormSet = formset_factory(RenewSingleForm)
    formset = RenewalFormSet(initial=[
                {'title' : 'Membership Renewal',
                 'date'  : local_date_now()}])
'''

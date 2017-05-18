#########################################################################
#
#   Astronomy Club Membership
#   file: membership/forms.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2017-06-01  Teruo Utsumi, initial code
#
#########################################################################

from django            import forms
from django.forms      import formset_factory, ModelForm
 
from sched_core.config import current_year, local_date_now
from sched_ev  .models import L_MONTH
from .models           import User

 
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

class NewForm(ModelForm):
    class Meta:
        model = User
        fields = ['date_start', 'date_end', 'date_since', 
                  'first_name', 'last_name',
                  'email',
                  'addr1', 'addr2',
                  'city', 'state', 'zip_code',
                  'phone1', 'phone2', 'notes']

class RenewForm(forms.Form):
    old_start  = forms.DateField(widget=forms.HiddenInput())
    old_end    = forms.DateField(widget=forms.HiddenInput())
    new_start  = forms.DateField()
    new_end    = forms.DateField()
    future     = forms.BooleanField(widget=forms.HiddenInput())
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

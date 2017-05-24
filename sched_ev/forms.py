from django import forms
 

class EventGenForm(forms.Form):
    date_start   = forms.DateField(label='start date'  )
    date_end     = forms.DateField(label='end date'    )

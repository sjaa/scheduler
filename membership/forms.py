from django import forms


class VerifyForm_Orion(forms.Form):
    first_name = forms.CharField(max_length=3)
    last_name  = forms.CharField(max_length=20)


class VerifyForm_Membership(forms.Form):
    email = forms.EmailField(max_length=40)

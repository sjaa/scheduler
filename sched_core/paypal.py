# pip install django-paypal

# https://django-paypal.readthedocs.io/

from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

def view_that_asks_for_money(request):

    URL = 'https://www.example.com'
    # What you want the button to do.
    paypal_dict = {
        'business': 'receiver_email@example.com',
        'amount': '10000000.00',
        'item_name': 'name of the item',
        'invoice': 'unique-invoice-id',
        'notify_url': URL + reverse('paypal-ipn'),
        'return_url': URL + '/paypal-complete/',
        'cancel_return': URL + '/paypal-cancel',
        'custom': 'Upgrade all users!',  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'payment.html', context)

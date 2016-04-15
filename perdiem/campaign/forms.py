"""
:Created: 14 April 2016
:Author: Lucas Connors

"""

from django import forms


class PaymentChargeForm(forms.Form):

    card = forms.CharField()
    num_shares = forms.IntegerField(min_value=1)

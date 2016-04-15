"""
:Created: 10 April 2016
:Author: Lucas Connors

"""

import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.edit import View

from pinax.stripe.actions import charges, customers

from campaign.forms import PaymentChargeForm
from campaign.models import Investment


class PaymentChargeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # Validate request
        request_dict = request.POST.copy()
        request_dict.update(request.GET)
        form = PaymentChargeForm(request_dict)
        if not form.is_valid():
            return HttpResponseBadRequest(unicode(form.errors))
        d = form.cleaned_data

        # Get card and customer
        card = d['card']
        customer = customers.get_customer_for_user(request.user)
        if not customer:
            customer = customers.create(request.user, card=card, plan=None, charge_immediately=False)

        # Create charge
        campaign = d['campaign']
        amount = decimal.Decimal(campaign.value_per_share)
        charge = charges.create(amount=amount, customer=customer.stripe_id)
        Investment.objects.create(charge=charge, campaign=campaign)
        return HttpResponse(status=205)

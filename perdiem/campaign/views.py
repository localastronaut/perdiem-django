"""
:Created: 10 April 2016
:Author: Lucas Connors

"""

import decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import View

from pinax.stripe.actions import charges, customers

from campaign.models import Campaign, Investment


class PaymentChargeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        # Get card and customer
        card = request.POST.get('stripeToken')
        customer = customers.get_customer_for_user(request.user)
        if not customer:
            customer = customers.create(request.user, card=card, plan=None, charge_immediately=False)

        # Create charge
        campaign_id = request.GET['campaign_id']
        campaign = Campaign.objects.get(id=campaign_id)
        amount = decimal.Decimal(campaign.value_per_share)
        charge = charges.create(amount=amount, customer=customer.stripe_id)
        Investment.objects.create(charge=charge, campaign=campaign)

        # Redirect to artist page
        return HttpResponseRedirect(reverse('artist', args=(campaign.artist.slug,)))

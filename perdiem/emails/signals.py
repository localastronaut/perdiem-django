"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from django.dispatch import receiver

from pinax.stripe.models import Charge
from pinax.stripe.webhooks import registry

from emails.messages import InvestSuccessEmail


@receiver(registry.get_signal("charge.succeeded"))
def charge_succeeded_handler(sender, **kwargs):
    # Get investment this successful charge is related to
    charge_id = kwargs['event'].message['data']['object']['id']
    charge = Charge.objects.get(stripe_id=charge_id)
    investment = charge.investment

    # Send out email for investing
    InvestSuccessEmail().send(user=investment.investor(), investment=investment)

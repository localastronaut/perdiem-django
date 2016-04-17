"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from django.dispatch import receiver

from pinax.stripe.models import Charge
from pinax.stripe.webhooks import registry
from templated_email import send_templated_mail


@receiver(registry.get_signal("charge.succeeded"))
def charge_succeeded_handler(sender, **kwargs):
    # Get investment this successful charge is related to
    charge_id = kwargs['event'].message['data']['object']['id']
    charge = Charge.objects.get(stripe_id=charge_id)
    investment = charge.investment

    # Send out email for investing
    investor = investment.investor()
    context = {
        'artist': investment.campaign.artist,
        'campaign': investment.campaign,
        'num_shares': investment.num_shares,
    }
    send_templated_mail(
        template_name='invest_success',
        from_email='noreply@investperdiem.com',
        recipient_list=[investor.email],
        context=context
    )

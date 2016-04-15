"""
:Created: 14 April 2016
:Author: Lucas Connors

"""

from django import forms

from campaign.models import Campaign


class PaymentChargeForm(forms.Form):

    card = forms.CharField()
    campaign = forms.IntegerField()

    def clean_campaign(self):
        campaign_id = self.cleaned_data['campaign']

        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            raise forms.ValidationError("Campaign with ID {campaign_id} does not exist.".format(campaign_id=campaign_id))

        return campaign

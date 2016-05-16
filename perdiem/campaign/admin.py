"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from django import forms
from django.contrib import admin

from pinax.stripe.models import (
    Charge, Customer, EventProcessingException, Event, Invoice, Plan, Transfer
)

from campaign.models import Campaign, Expense, Investment, RevenueReport


# Unregister Pinax Stripe models from admin
for pinax_stripe_model in [
    Charge, Customer, EventProcessingException, Event, Invoice, Plan, Transfer
]:
    admin.site.unregister(pinax_stripe_model)


class CampaignAdminForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ('artist', 'amount', 'reason', 'value_per_share', 'start_datetime', 'end_datetime', 'use_of_funds', 'fans_percentage',)

    def clean(self):
        cleaned_data = super(CampaignAdminForm, self).clean()
        end_datetime = cleaned_data['end_datetime']
        if end_datetime and end_datetime < cleaned_data['start_datetime']:
            raise forms.ValidationError("Campaign cannot end before it begins.")
        return cleaned_data


class ExpenseInline(admin.TabularInline):

    model = Expense


class CampaignAdmin(admin.ModelAdmin):

    form = CampaignAdminForm
    inlines = (ExpenseInline,)


class InvestmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'campaign', 'investor', 'transaction_datetime', 'num_shares',)
    readonly_fields = map(lambda f: f.name, Investment._meta.get_fields())

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(RevenueReport)

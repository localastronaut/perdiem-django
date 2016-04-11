"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from django.contrib import admin
from django.contrib.sites.models import Site

from pinax.stripe.models import Charge, Customer, EventProcessingException, \
    Event, Invoice, Plan, Transfer

from campaign.models import Campaign, Expense, Investment, RevenueReport


# Unregister Pinax Stripe models (and Site) from admin
for pinax_stripe_model in [
    Charge, Customer, EventProcessingException, Event, Invoice, Plan, Transfer
]:
    admin.site.unregister(pinax_stripe_model)
admin.site.unregister(Site)


class ExpenseInline(admin.TabularInline):

    model = Expense


class CampaignAdmin(admin.ModelAdmin):

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

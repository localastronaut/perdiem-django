"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from django.contrib import admin

from campaign.models import Campaign, Expense, RevenueReport


class ExpenseInline(admin.TabularInline):

    model = Expense


class CampaignAdmin(admin.ModelAdmin):

    inlines = (ExpenseInline,)


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(RevenueReport)

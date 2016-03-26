"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from django.contrib import admin

from campaign.models import Campaign, Expense, Investment, RevenueReport


class ExpenseInline(admin.TabularInline):

    model = Expense


class CampaignAdmin(admin.ModelAdmin):

    inlines = (ExpenseInline,)


class InvestmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'campaign', 'user', 'transaction_datetime', 'num_shares',)
    readonly_fields = map(lambda f: f.name, Investment._meta.get_fields())

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(RevenueReport)

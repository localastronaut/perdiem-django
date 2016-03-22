"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone

from artist.models import Artist


class Campaign(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(help_text='The amount of money the artist wishes to raise')
    reason = models.CharField(max_length=40, help_text='The reason why the artist is raising money, in a few words')
    value_per_share = models.PositiveIntegerField(default=1, help_text='The value (in dollars) per share the artist wishes to sell')
    start_datetime = models.DateTimeField(db_index=True, default=timezone.now, help_text='When the campaign will start accepting investors')
    end_datetime = models.DateTimeField(db_index=True, null=True, blank=True, help_text='When the campaign ends and will no longer accept investors (no end date if blank)')
    use_of_funds = models.TextField(null=True, blank=True, help_text='A description of how the funds will be used')
    fans_percentage = models.PositiveSmallIntegerField(help_text='The percentage of revenue that goes back to the fans (a value from 0-100)')

    def __unicode__(self):
        return u'{artist}: ${amount} {reason}'.format(
            artist=unicode(self.artist),
            amount=self.amount,
            reason=self.reason
        )

    def total_shares_purchased(self):
        return self.investment_set.all().aggregate(total_shares=Sum('num_shares'))['total_shares'] or 0

    def amount_raised(self):
        return self.total_shares_purchased() * self.value_per_share

    def percentage_funded(self):
        try:
            return "{0:.2f}".format(float(self.amount_raised()) / self.amount)
        except ZeroDivisionError:
            return 0

    def num_investors(self):
        return self.investment_set.all().aggregate(num_investors=Count('user'))['num_investors']

    def days_remaining(self):
        if self.end_datetime:
            return max(0, (self.end_datetime - timezone.now()).days)

    def num_shares(self):
        return self.amount / self.value_per_share

    def artist_percentage(self):
        return 100 - self.fans_percentage

    def revenue_to_2x(self):
        return self.amount * (100/self.fans_percentage) * 2


class Expense(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    expense = models.CharField(max_length=30, help_text='A description of one of the expenses for the artist (eg. Studio cost)')

    class Meta:
        unique_together = (('campaign', 'expense',))

    def __unicode__(self):
        return u'{campaign} ({expense})'.format(
            campaign=unicode(self.campaign),
            expense=self.expense
        )


class Investment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    transaction_datetime = models.DateTimeField(db_index=True, auto_now_add=True)
    num_shares = models.PositiveSmallIntegerField(default=1, help_text='The number of shares a user made in a transaction')

    def __unicode__(self):
        return u'{num_shares} shares in {campaign} to {user}'.format(
            num_shares=self.num_shares,
            campaign=unicode(self.campaign),
            user=unicode(self.user)
        )


class RevenueReport(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(help_text='The amount of revenue generated (in dollars) being reported (since last report)')
    reported_datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'${amount} for {campaign}'.format(
            amount=self.amount,
            campaign=unicode(self.campaign)
        )

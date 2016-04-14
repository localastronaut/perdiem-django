"""
:Created: 5 April 2016
:Author: Lucas Connors

"""

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from accounts.forms import RegisterAccountForm
from artist.models import Artist
from campaign.models import Campaign, Investment


class RegisterAccountView(CreateView):

    template_name = 'registration/register.html'
    form_class = RegisterAccountForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        valid = super(RegisterAccountView, self).form_valid(form)

        # Login the newly-registered user
        d = form.cleaned_data
        username, password = d['username'], d['password1']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)

        return valid


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # Get artists the user has invested in
        investments = Investment.objects.filter(charge__customer__user=self.request.user)
        campaign_ids = investments.values_list('campaign', flat=True).distinct()
        campaigns = Campaign.objects.filter(id__in=campaign_ids)
        artist_ids = campaigns.values_list('artist', flat=True).distinct()
        context['artists'] = Artist.objects.filter(id__in=artist_ids)

        # Update context with total investments
        aggregate_context = investments.aggregate(
            total_investments=models.Sum(
                models.F('campaign__value_per_share') * models.F('num_shares'),
                output_field=models.FloatField()
            )
        )
        context.update(aggregate_context)

        # Update context with total earned
        total_earned = 0
        for campaign in campaigns:
            num_shares_this_campaign = investments.filter(campaign=campaign).aggregate(ns=models.Sum('num_shares'))['ns']
            total_earned += campaign.generated_revenue_fans_per_share() * num_shares_this_campaign
        context['total_earned'] = total_earned

        return context

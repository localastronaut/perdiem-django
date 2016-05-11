"""
:Created: 5 April 2016
:Author: Lucas Connors

"""

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from accounts.forms import RegisterAccountForm, EditNameForm, ContactForm
from artist.models import Artist, Update
from campaign.models import Campaign, Investment
from emails.messages import WelcomeEmail, ContactEmail
from emails.models import EmailSubscription


class RegisterAccountView(CreateView):

    template_name = 'registration/register.html'
    form_class = RegisterAccountForm

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        valid = super(RegisterAccountView, self).form_valid(form)

        # Login the newly-registered user
        d = form.cleaned_data
        username, password = d['username'], d['password1']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)

        # Create the user's newsletter subscription (if applicable)
        if d['subscribe_news']:
            EmailSubscription.objects.create(user=user, subscription=EmailSubscription.SUBSCRIPTION_NEWS)

        # Send user welcome email
        WelcomeEmail().send(user=user)

        return valid


class MultipleFormView(TemplateView):

    def get_form_classes(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(MultipleFormView, self).get_context_data(**kwargs)

        for form_name, attrs in self.get_form_classes().iteritems():
            if attrs['context_name'] not in context:
                form_kwargs = {
                    'initial': attrs['get_initial'](),
                }
                if self.request.method == 'POST' and self.request.POST.get('action') == form_name:
                    form_kwargs['data'] = self.request.POST
                context[attrs['context_name']] = attrs['class'](self.request.user, **form_kwargs)

        return context

    def post(self, request, *args, **kwargs):
        try:
            form_name = request.POST['action']
            form_attrs = self.get_form_classes()[form_name]
        except KeyError:
            return HttpResponseBadRequest("Form action unrecognized or unspecified.")

        form = form_attrs['class'](self.request.user, request.POST)
        if form.is_valid():
            form_attrs['form_valid'](form)
        else:
            kwargs.update({form_attrs['context_name']: form,})
        return self.render_to_response(self.get_context_data(**kwargs))


class ProfileView(LoginRequiredMixin, MultipleFormView):

    template_name = 'registration/profile.html'

    def get_form_classes(self):
        return {
            'edit_name': {
                'class': EditNameForm,
                'context_name': 'edit_name_form',
                'get_initial': self.edit_name_get_initial,
                'form_valid': self.edit_name_form_valid,
            },
            'change_password': {
                'class': PasswordChangeForm,
                'context_name': 'change_password_form',
                'get_initial': lambda: {},
                'form_valid': self.change_password_form_valid,
            },
        }

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # Get artists the user has invested in
        investments = Investment.objects.filter(charge__customer__user=self.request.user, charge__paid=True)
        campaign_ids = investments.values_list('campaign', flat=True).distinct()
        campaigns = Campaign.objects.filter(id__in=campaign_ids)
        artist_ids = campaigns.values_list('artist', flat=True).distinct()
        artists = Artist.objects.filter(id__in=artist_ids)
        context['artists'] = artists
        context['updates'] = Update.objects.filter(artist__in=artists).order_by('-created_datetime')

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

    def edit_name_get_initial(self):
        user = self.request.user
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'invest_anonymously': user.userprofile.invest_anonymously,
        }

    def edit_name_form_valid(self, form):
        user = self.request.user
        d = form.cleaned_data

        # Update username and name
        user.username = d['username']
        user.first_name = d['first_name']
        user.last_name = d['last_name']
        user.save()

        # Update anonymity
        user.userprofile.invest_anonymously = d['invest_anonymously']
        user.userprofile.save()

    def change_password_form_valid(self, form):
        user = self.request.user
        d = form.cleaned_data

        # Update user's password
        user.set_password(d['new_password1'])
        user.save()


class PublicProfileView(TemplateView):

    template_name = 'registration/public_profile.html'

    def get_context_data(self, **kwargs):
        context = super(PublicProfileView, self).get_context_data(**kwargs)
        profile_user = User.objects.get(username=kwargs['username'])
        artists = Artist.objects.filter(campaign__investment__charge__customer__user=profile_user).distinct()

        context.update({
            'profile_user': profile_user,
            'artists': artists,
            'updates': Update.objects.filter(artist__in=artists).order_by('-created_datetime'),
        })
        return context


class ContactFormView(FormView):

    template_name = 'registration/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contact_thanks')

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        user = self.request.user
        if user.is_authenticated():
            initial['email'] = user.email
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        # Add user_id to context, if available
        context = form.cleaned_data
        user = self.request.user
        if user.is_authenticated():
            context['user_id'] = user.id

        # Send contact email
        ContactEmail().send_to_email(email='support@investperdiem.com', context=context)

        return super(ContactFormView, self).form_valid(form)

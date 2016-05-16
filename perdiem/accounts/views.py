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
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView

from accounts.forms import (
    RegisterAccountForm, EditNameForm, EditAvatarForm, EmailPreferencesForm,
    ContactForm
)
from accounts.models import UserAvatar, UserAvatarImage
from artist.models import Artist, Update
from campaign.models import Campaign, Investment
from emails.messages import WelcomeEmail, ContactEmail
from emails.models import EmailSubscription
from perdiem.views import ConstituentFormView, MultipleFormView


class RegisterAccountView(CreateView):

    template_name = 'registration/register.html'
    form_class = RegisterAccountForm

    def get_success_url(self):
        return self.request.GET.get('next') or reverse('profile')

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


class EditNameFormView(ConstituentFormView):

    form_class = EditNameForm
    provide_user = True

    def get_initial(self):
        user = self.request.user
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'invest_anonymously': user.userprofile.invest_anonymously,
        }

    def form_valid(self, form):
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


class EditAvatarFormView(ConstituentFormView):

    form_class = EditAvatarForm
    provide_user = True
    includes_files = True

    def get_initial(self):
        user_profile = self.request.user.userprofile
        return {
            'avatar': user_profile.avatar.id if user_profile.avatar else '',
        }

    def form_valid(self, form):
        user = self.request.user
        d = form.cleaned_data

        # Upload a custom avatar, if provided
        user_avatar = d['avatar']
        custom_avatar = d['custom_avatar']
        if custom_avatar:
            user_avatar, _ = UserAvatar.objects.get_or_create(user=user, provider=UserAvatar.PROVIDER_PERDIEM)
            UserAvatarImage.objects.update_or_create(avatar=user_avatar, defaults={'img': custom_avatar,})

        # Update user's avatar
        user.userprofile.avatar = user_avatar
        user.userprofile.save()


class ChangePasswordFormView(ConstituentFormView):

    form_class = PasswordChangeForm
    provide_user = True

    def form_valid(self, form):
        user = self.request.user
        d = form.cleaned_data

        # Update user's password
        user.set_password(d['new_password1'])
        user.save()


class EmailPreferencesFormView(ConstituentFormView):

    form_class = EmailPreferencesForm

    def get_initial(self):
        initial = {}
        for subscription_type, _ in EmailSubscription.SUBSCRIPTION_CHOICES:
            subscribed = EmailSubscription.objects.is_subscribed(user=self.request.user, subscription_type=subscription_type)
            initial['subscription_{stype}'.format(stype=subscription_type.lower())] = subscribed
        return initial

    def form_valid(self, form):
        user = self.request.user

        # Update user's email subscriptions
        email_subscriptions = {k: v for k, v in form.cleaned_data.iteritems() if k.startswith('subscription_')}
        for subscription_type, is_subscribed in email_subscriptions.iteritems():
            EmailSubscription.objects.update_or_create(
                user=user,
                subscription=getattr(EmailSubscription, subscription_type.upper()),
                defaults={'subscribed': is_subscribed,}
            )


class ProfileView(LoginRequiredMixin, MultipleFormView):

    template_name = 'registration/profile.html'
    constituent_form_views = {
        'edit_name': EditNameFormView,
        'edit_avatar': EditAvatarFormView,
        'change_password': ChangePasswordFormView,
        'email_preferences': EmailPreferencesFormView,
    }

    @staticmethod
    def prepare_artist_for_context(artist):
        artist.total_invested = 0
        artist.total_earned = 0
        return artist.id, artist

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # Get artists the user has invested in
        investments = Investment.objects.filter(charge__customer__user=self.request.user, charge__paid=True)
        campaign_ids = investments.values_list('campaign', flat=True).distinct()
        campaigns = Campaign.objects.filter(id__in=campaign_ids)
        artist_ids = campaigns.values_list('artist', flat=True).distinct()
        artists = Artist.objects.filter(id__in=artist_ids)
        context['artists'] = dict(map(self.prepare_artist_for_context, artists))
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
            artist = campaign.artist
            num_shares_this_campaign = investments.filter(campaign=campaign).aggregate(ns=models.Sum('num_shares'))['ns']
            generated_revenue_user = campaign.generated_revenue_fans_per_share() * num_shares_this_campaign
            context['artists'][artist.id].total_invested += num_shares_this_campaign * campaign.value_per_share
            context['artists'][artist.id].total_earned += generated_revenue_user
            total_earned += generated_revenue_user
        context['total_earned'] = total_earned

        # Update context with available avatars
        user_avatars = UserAvatar.objects.filter(user=self.request.user)
        avatars = {
            'Default': UserAvatar.default_avatar_url(),
        }
        avatars.update({avatar.get_provider_display(): avatar.avatar_url() for avatar in user_avatars})
        context['avatars'] = avatars

        return context


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

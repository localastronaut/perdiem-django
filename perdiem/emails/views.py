"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from emails.models import EmailSubscription
from emails.utils import check_token


class UnsubscribeView(TemplateView):

    template_name = 'registration/unsubscribe.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        return super(UnsubscribeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnsubscribeView, self).get_context_data(**kwargs)
        if (self.request.user.is_authenticated() and self.request.user == self.user) or check_token(self.user, kwargs['token']):
            EmailSubscription.objects.unsubscribe_user(self.user)
            context['success'] = True
            context['email'] = self.user.email
        else:
            context['success'] = False
        return context

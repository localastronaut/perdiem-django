"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from django.db import models


class EmailSubscriptionManager(models.Manager):

    def is_subscribed(self, user):
        try:
            subscription = self.get(user=user)
        except self.model.DoesNotExist:
            return True
        else:
            return subscription.subscribed

    def unsubscribe_user(self, user):
        self.get_or_create(user=user, defaults={'subscribed': False,})

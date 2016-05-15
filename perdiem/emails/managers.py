"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from django.db import models


class EmailSubscriptionManager(models.Manager):

    def is_subscribed(self, user, subscription_type=None):
        if not subscription_type:
            subscription_type = self.model.SUBSCRIPTION_ALL

        try:
            subscription = self.get(user=user, subscription=subscription_type)
        except self.model.DoesNotExist:
            return True if subscription_type == self.model.SUBSCRIPTION_ALL else False
        else:
            return subscription.subscribed

    def unsubscribe_user(self, user, subscription_type=None):
        if not subscription_type:
            subscription_type = self.model.SUBSCRIPTION_ALL
        self.update_or_create(user=user, subscription=subscription_type, defaults={'subscribed': False,})

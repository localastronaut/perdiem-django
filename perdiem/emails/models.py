"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from emails.managers import EmailSubscriptionManager


class EmailSubscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)

    objects = EmailSubscriptionManager()

    def __unicode__(self):
        return unicode(self.user)

"""
:Created: 5 May 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invest_anonymously = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user)

    def get_display_name(self):
        if self.invest_anonymously:
            return 'Anonymous'
        else:
            return self.user.get_full_name() or self.user.username

    def public_profile_url(self):
        if not self.invest_anonymously:
            return reverse('public_profile', args=(self.user.username,))

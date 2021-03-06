"""
:Created: 5 May 2016
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver

from accounts.models import UserProfile


@receiver(models.signals.post_save, sender=User, dispatch_uid="userprofile_autocreate_handler")
def userprofile_autocreate_handler(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']

    if created:
        UserProfile.objects.create(user=user)

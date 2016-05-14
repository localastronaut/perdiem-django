"""
:Created: 5 May 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class UserAvatar(models.Model):

    PROVIDER_PERDIEM = 'perdiem'
    PROVIDER_GOOGLE = 'google-oauth2'
    PROVIDER_FACEBOOK = 'facebook'
    PROVIDER_CHOICES = (
        (PROVIDER_PERDIEM, 'PerDiem'),
        (PROVIDER_GOOGLE, 'Google'),
        (PROVIDER_FACEBOOK, 'Facebook'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(choices=PROVIDER_CHOICES, max_length=15)

    class Meta:
        unique_together = (('user', 'provider',),)

    def __unicode__(self):
        return u'{user}: {provider}'.format(
            user=unicode(self.user),
            provider=self.get_provider_display()
        )


class UserAvatarURL(models.Model):

    avatar = models.OneToOneField(UserAvatar, on_delete=models.CASCADE)
    url = models.URLField()

    def __unicode__(self):
        return unicode(self.avatar)


class UserAvatarImage(models.Model):

    avatar = models.OneToOneField(UserAvatar, on_delete=models.CASCADE)
    img = models.ImageField()

    def __unicode__(self):
        return unicode(self.avatar)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(UserAvatar, null=True, blank=True)
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

    def default_avatar_url(self):
        return "{static_url}img/avatar.jpg".format(static_url=settings.STATIC_URL)

    def avatar_url(self):
        if not self.avatar:
            return self.default_avatar_url()
        elif self.avatar.provider in [UserAvatar.PROVIDER_GOOGLE, UserAvatar.PROVIDER_FACEBOOK]:
            return self.avatar.useravatarurl.url
        elif self.avatar.provider == UserAvatar.PROVIDER_PERDIEM:
            return self.avatar.useravatarimage.img.url
        else:
            return self.default_avatar_url()

    def display_avatar_url(self):
        if self.invest_anonymously:
            return self.default_avatar_url()
        return self.avatar_url()

"""
:Created: 5 May 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from sorl.thumbnail import get_thumbnail


class UserAvatar(models.Model):

    PROVIDER_PERDIEM = 'perdiem'
    PROVIDER_GOOGLE = 'google-oauth2'
    PROVIDER_FACEBOOK = 'facebook'
    PROVIDER_CHOICES = (
        (PROVIDER_PERDIEM, 'Custom'),
        (PROVIDER_GOOGLE, 'Google'),
        (PROVIDER_FACEBOOK, 'Facebook'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(choices=PROVIDER_CHOICES, max_length=15)

    class Meta:
        unique_together = (('user', 'provider',),)

    @staticmethod
    def default_avatar_url():
        return "{static_url}img/avatar.jpg".format(static_url=settings.STATIC_URL)

    def __unicode__(self):
        return u'{user}: {provider}'.format(
            user=unicode(self.user),
            provider=self.get_provider_display()
        )

    def avatar_url(self):
        if self.provider in [self.PROVIDER_GOOGLE, self.PROVIDER_FACEBOOK]:
            return self.useravatarurl.url
        elif self.provider == self.PROVIDER_PERDIEM:
            original = self.useravatarimage.img
            return get_thumbnail(original, '50x50', crop='center').url
        else:
            return self.default_avatar_url()


class UserAvatarURL(models.Model):

    avatar = models.OneToOneField(UserAvatar, on_delete=models.CASCADE)
    url = models.URLField()

    def __unicode__(self):
        return unicode(self.avatar)


class UserAvatarImage(models.Model):

    def user_avatar_filename(instance, filename):
        extension = filename.split('.')[-1]
        new_filename = '{user_id}.{extension}'.format(
            user_id=instance.avatar.user.id,
            extension=extension
        )
        return '/'.join(['avatars', new_filename,])

    avatar = models.OneToOneField(UserAvatar, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=user_avatar_filename)

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

    def avatar_url(self):
        if not self.avatar:
            return UserAvatar.default_avatar_url()
        return self.avatar.avatar_url()

    def display_avatar_url(self):
        if self.invest_anonymously:
            return UserAvatar.default_avatar_url()
        return self.avatar_url()

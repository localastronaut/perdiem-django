"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from artist.managers import ArtistQuerySet


class Genre(models.Model):

    name = models.CharField(max_length=40, db_index=True, unique=True)

    def __unicode__(self):
        return self.name


class Artist(models.Model):

    name = models.CharField(max_length=60, db_index=True)
    genres = models.ManyToManyField(Genre)
    slug = models.SlugField(max_length=40, unique=True, help_text='A short label for an artist (used in URLs)')
    lat = models.DecimalField(max_digits=6, decimal_places=4, db_index=True, help_text='Latitude of artist location')
    lon = models.DecimalField(max_digits=7, decimal_places=4, db_index=True, help_text='Longitude of artist location')
    location = models.CharField(max_length=40, help_text='Description of artist location (usually city, state, country format)')

    objects = ArtistQuerySet.as_manager()

    def __unicode__(self):
        return self.name

    def latest_campaign(self):
        campaigns = self.campaign_set.all().order_by('-start_datetime')
        if campaigns:
            return campaigns[0]

    def active_campaign(self):
        active_campaigns = self.campaign_set.filter(start_datetime__lt=timezone.now(), end_datetime__gte=timezone.now()).order_by('-start_datetime')
        if active_campaigns:
            return active_campaigns[0]

    def past_campaigns(self):
        return self.campaign_set.filter(end_datetime__lt=timezone.now()).order_by('-end_datetime')


class Bio(models.Model):

    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    bio = models.TextField(help_text='Short biography of artist. May contain HTML.')

    def __unicode__(self):
        return unicode(self.artist)


class Photo(models.Model):

    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='artist', help_text='Primary profile photo of artist')

    def __unicode__(self):
        return unicode(self.artist)


class SoundCloudPlaylist(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    playlist = models.URLField(unique=True, help_text='The SoundCloud iframe URL to the artist\'s playlist')

    def __unicode__(self):
        return self.playlist


class Social(models.Model):

    SOCIAL_CHOICES = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('soundcloud', 'SoundCloud'),
    )

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    medium = models.CharField(choices=SOCIAL_CHOICES, max_length=10, help_text='The type of social network')
    url = models.URLField(unique=True, help_text='The URL to the artist\'s social network page')

    class Meta:
        unique_together = (('artist', 'medium',),)

    def __unicode__(self):
        return u'{artist}: {medium}'.format(
            artist=unicode(self.artist),
            medium=self.get_medium_display()
        )


class Update(models.Model):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(db_index=True, auto_now_add=True)
    text = models.TextField(help_text='The content of the update. May contain HTML.')

    def __unicode__(self):
        return u'{artist}: {datetime}'.format(
            artist=unicode(self.artist),
            datetime=self.created_datetime.strftime('%m-%d-%Y')
        )

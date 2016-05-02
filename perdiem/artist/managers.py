"""
:Created: 1 May 2016
:Author: Lucas Connors

"""

from django.db import models

from geopy.distance import distance as calc_distance


class ArtistQuerySet(models.QuerySet):

    def filter_by_location(self, distance, lat, lon):
        nearby_artist_ids = []
        for artist in self.all():
            if calc_distance((lat, lon,), (artist.lat, artist.lon,)).miles <= distance:
                nearby_artist_ids.append(artist.id)
        return self.filter(id__in=nearby_artist_ids)

"""
:Created: 1 May 2016
:Author: Lucas Connors

"""

from django.db import models

import geopy
from geopy.distance import distance as calc_distance


class ArtistQuerySet(models.QuerySet):

    @staticmethod
    def bounding_coordinates(distance, lat, lon):
        origin = geopy.Point((lat, lon,))
        geopy_distance = calc_distance(miles=distance)
        min_lat = geopy_distance.destination(origin, 180).latitude
        max_lat = geopy_distance.destination(origin, 0).latitude
        min_lon = geopy_distance.destination(origin, 270).longitude
        max_lon = geopy_distance.destination(origin, 90).longitude
        return min_lat, max_lat, min_lon, max_lon

    @staticmethod
    def percentage_funded(artist):
        campaign = artist.latest_campaign()
        if campaign:
            funded = campaign.percentage_funded()
            artist.funded = funded
            return funded

    def filter_by_location(self, distance, lat, lon):
        min_lat, max_lat, min_lon, max_lon = self.bounding_coordinates(distance, lat, lon)
        artists_within_bounds = self.filter(
            lat__gte=min_lat,
            lat__lte=max_lat,
            lon__gte=min_lon,
            lon__lte=max_lon
        )

        nearby_artist_ids = []
        for artist in artists_within_bounds:
            if calc_distance((lat, lon,), (artist.lat, artist.lon,)).miles <= distance:
                nearby_artist_ids.append(artist.id)
        return self.filter(id__in=nearby_artist_ids)

    # TODO(lucas): Use annotations as much as possible to improve performance
    def order_by_percentage_funded(self):
        return sorted(self, key=self.percentage_funded, reverse=True)

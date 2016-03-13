"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

from perdiem.tests import PerDiemTestCase


class ArtistAdminWebTestCase(PerDiemTestCase):

    def get200s(self):
        return [
            '/admin/artist/',
            '/admin/artist/genre/',
            '/admin/artist/genre/add/',
            '/admin/artist/genre/{genre_id}/change/'.format(genre_id=self.genre.id),
            '/admin/artist/artist/',
            '/admin/artist/artist/add/',
            '/admin/artist/artist/{artist_id}/change/'.format(artist_id=self.artist.id),
            '/admin/artist/update/',
            '/admin/artist/update/add/',
            '/admin/artist/update/{update_id}/change/'.format(update_id=self.update.id),
        ]

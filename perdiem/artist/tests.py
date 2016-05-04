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


class ArtistWebTestCase(PerDiemTestCase):

    def get200s(self):
        return [
            '/artists/',
            '/artists/?distance=50&lat=43.7689&lon=-79.4138',
            '/artists/?distance=50&location=Toronto,%20ON',
            '/artists/?sort=recent',
            '/artists/?sort=funded',
            '/artist/apply/',
            '/artist/{slug}/'.format(slug=self.artist.slug),
        ]

    def testArtistDoesNotExistReturns404(self):
        self.assertResponseRenders('/artist/does-not-exist/', status_code=404)

    def testArtistApplication(self):
        self.assertResponseRedirects(
            '/artist/apply/',
            '/artist/apply/thanks',
            method='POST',
            data={
                'artist_name': 'Segmentation Fault',
                'genre': 'Heavy Metal',
                'hometown': 'Waterloo, ON, Canada',
                'email': self.user.email,
                'phone_number': '(226) 123-4567',
                'bio': 'We are a really cool heavy metal band. We mostly perform covers but are excited to create an album, and we\'re hoping PerDiem can help us do that.',
                'campaign_reason': 'We want to record our next album: Access Granted.',
                'campaign_expenses': 'Studio time, mastering, mixing, etc.',
                'music_link': 'https://www.spotify.com/',
                'terms': True,
            }
        )


class CoordinatesFromAddressTestCase(PerDiemTestCase):

    url = '/api/coordinates/?address={address}'
    valid_url = url.format(address='Willowdale%2C+Toronto%2C+Ontario%2C+Canada')

    def testCoordinatesFromAddress(self):
        response = self.assertJsonResponseRenders(self.valid_url)
        lat, lon = response['latitude'], response['longitude']
        self.assertAlmostEquals(lat, 43.7689, places=2)
        self.assertAlmostEquals(lon, -79.4138, places=2)

    def testCoordinatesFromAddressRequiresAddress(self):
        for url in ['/api/coordinates/', self.url.format(address=''),]:
            self.assertResponseRenders(url, status_code=400)

    def testCoordinatesFromAddressFailsWithoutPermission(self):
        # Logout from being a superuser
        self.client.logout()

        # Coordinates from Address API requires permission
        # but you're not authenticated
        self.assertResponseRenders(self.valid_url, status_code=403)

        # Login as an ordinary user
        self.client.login(
            username=self.ORDINARY_USER_USERNAME,
            password=self.USER_PASSWORD
        )

        # Coordinates from Address API requires permission
        # but you don't have the required permission
        self.assertResponseRenders(self.valid_url, status_code=403)

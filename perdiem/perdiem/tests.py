"""
:Created: 5 March 2016
:Author: Lucas Connors

"""

from django.contrib.auth.models import User
from django.test import TestCase


class PerDiemTestCase(TestCase):

    USER_USERNAME = 'jsmith'
    USER_EMAIL = 'jsmith@example.com'
    USER_PASSWORD = 'abc123'

    def setUp(self):
        super(PerDiemTestCase, self).setUp()
        self.user = User.objects.create_user(
            self.USER_USERNAME,
            email=self.USER_EMAIL,
            password=self.USER_PASSWORD
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.login(
            username=self.USER_USERNAME,
            password=self.USER_PASSWORD
        )

    def tearDown(self):
        User.objects.all().delete()
        super(PerDiemTestCase, self).tearDown()


class PerDiemHomeWebTestCase(PerDiemTestCase):

    def testHomePageRenders(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)


class AdminHomeWebTestCase(PerDiemTestCase):

    def testAdminHomePageRenders(self):
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)


class AdminLoginWebTestCase(PerDiemTestCase):

    @staticmethod
    def strip_query_params(url):
        return url.split('?')[0]

    def testAdminLoginPageRenders(self):
        self.client.logout()
        response = self.client.get('/admin/', follow=True)
        url, status_code = response.redirect_chain[0]
        self.assertEquals(status_code, 302)
        self.assertEquals(self.strip_query_params(url), '/admin/login/')

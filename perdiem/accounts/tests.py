"""
:Created: 5 April 2016
:Author: Lucas Connors

"""

from perdiem.tests import PerDiemTestCase


class PerDiemHomeWebTestCase(PerDiemTestCase):

    def get200s(self):
        return [
            '/',
            '/faq/',
            '/404/',
            '/500/',
            '/trust/',
            '/terms/',
            '/privacy/',
            '/contact/',
            '/accounts/register/',
            '/accounts/profile/',
        ]

    def testHomePageUnauthenticated(self):
        self.client.logout()
        self.assertResponseRenders('/')

    def testLogout(self):
        self.assertResponseRedirects('/accounts/logout/', '/')

    def testLogin(self):
        self.client.logout()
        login_data = {
            'login-username': self.USER_USERNAME,
            'login-password': self.USER_PASSWORD,
        }
        response = self.assertResponseRenders('/', method='POST', data=login_data)
        self.assertIn('Logout', response.content)

    def testRegister(self):
        self.client.logout()
        self.assertResponseRedirects(
            '/accounts/register/',
            '/',
            method='POST',
            data={
                'username': 'msmith',
                'email': 'msmith@example.com',
                'password1': self.USER_PASSWORD,
                'password2': self.USER_PASSWORD,
            }
        )

    def testContact(self):
        self.assertResponseRedirects(
            '/contact/',
            '/contact/thanks',
            method='POST',
            data={'inquiry': 'General Inquiry', 'email': 'msmith@example.com', 'message': 'Hello World!',}
        )

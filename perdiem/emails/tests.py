"""
:Created: 17 April 2016
:Author: Lucas Connors

"""

from emails.utils import create_unsubscribe_link
from perdiem.tests import PerDiemTestCase


class UnsubscribeWebTestCase(PerDiemTestCase):

    def testUnsubscribe(self):
        unsubscribe_url = create_unsubscribe_link(self.user)
        self.assertResponseRenders(unsubscribe_url)

from __future__ import unicode_literals

from django.apps import AppConfig


class EmailsConfig(AppConfig):

    name = 'emails'

    def ready(self):
        import emails.signals

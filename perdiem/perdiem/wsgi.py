"""
WSGI config for perdiem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

import cbsettings
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perdiem.settings")
cbsettings.configure('perdiem.settings.switcher')

application = DjangoWhiteNoise(get_wsgi_application())

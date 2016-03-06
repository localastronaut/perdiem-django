"""
Django settings for perdiem project.
:Created: 5 March 2016
:Author: Lucas Connors

"""

import os

from cbsettings import switcher


SETTINGS_DIR = os.path.dirname(__file__)

dev_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'dev.py'))
prod_settings_exists = os.path.isfile(os.path.join(SETTINGS_DIR, 'prod.py'))

from perdiem.settings.travis import TravisSettings
switcher.register(TravisSettings, 'TRAVIS' in os.environ)

if dev_settings_exists:
    from perdiem.settings.dev import DevSettings
    switcher.register(DevSettings, dev_settings_exists and not prod_settings_exists)

if prod_settings_exists:
    from perdiem.settings.prod import ProdSettings
    switcher.register(ProdSettings, prod_settings_exists)

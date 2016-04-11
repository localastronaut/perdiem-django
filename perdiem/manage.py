#!/usr/bin/env python
import os
import sys
import warnings

from django.utils.deprecation import RemovedInDjango20Warning

# Propagate warnings as errors when running tests
if len(sys.argv) >= 2 and sys.argv[1] == 'test':
    warnings.filterwarnings('error')
    # This warning is raised by pinax-stripe, so we will have to ignore it for now
    warnings.filterwarnings("ignore", category=RemovedInDjango20Warning, message='on_delete will be a required arg for .*')

import cbsettings


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perdiem.settings")
    cbsettings.configure('perdiem.settings.switcher')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

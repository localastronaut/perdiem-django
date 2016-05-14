"""
:Created: 13 May 2016
:Author: Lucas Connors

"""

from django.shortcuts import render_to_response


def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if not details.get('email'):
        return render_to_response('registration/error_email_required.html')

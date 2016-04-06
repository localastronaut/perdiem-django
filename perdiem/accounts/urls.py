"""
:Created: 26 July 2015
:Author: Lucas Connors

"""

from django.conf.urls import url
from django.contrib.auth.views import login, logout

from accounts.views import RegisterAccountView


urlpatterns = [
    url(r'^login/?$', login, name='login'),
    url(r'^logout/?$', logout, {'next_page': '/',}, name='logout'),
    url(r'^register/?$', RegisterAccountView.as_view(), name='register'),
]

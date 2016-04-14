"""
:Created: 26 July 2015
:Author: Lucas Connors

"""

from django.conf.urls import url
from django.contrib.auth.views import logout

from accounts.views import RegisterAccountView, ProfileView


urlpatterns = [
    url(r'^logout/?$', logout, {'next_page': '/',}, name='logout'),
    url(r'^register/?$', RegisterAccountView.as_view(), name='register'),
    url(r'^profile/?$', ProfileView.as_view(), name='profile'),
]

"""
:Created: 26 July 2015
:Author: Lucas Connors

"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from artist.views import CoordinatesFromAddressView, ArtistListView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/coordinates/?$', CoordinatesFromAddressView.as_view(), name='coordinates'),
    url(r'^artists/?$', ArtistListView.as_view(), name='artists'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
]

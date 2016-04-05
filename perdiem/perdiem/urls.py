"""
:Created: 26 July 2015
:Author: Lucas Connors

"""

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView
from django.views.static import serve

from artist.views import CoordinatesFromAddressView, ArtistListView, \
    ArtistDetailView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/?$', login, name='login'),
    url(r'^accounts/logout/?$', logout, {'next_page': '/',}, name='logout'),
    url(r'^api/coordinates/?$', CoordinatesFromAddressView.as_view(), name='coordinates'),

    url(r'^artists/?$', ArtistListView.as_view(), name='artists'),
    url(r'^artist/(?P<slug>[\w_-]+)/?$', ArtistDetailView.as_view(), name='artist'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Add media folder to urls when DEBUG = True
if settings.DEBUG:
    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    )

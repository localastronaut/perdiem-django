"""
:Created: 19 March 2016
:Author: Lucas Connors

"""

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.list import ListView

from geopy.distance import distance
from geopy.geocoders import Nominatim

from artist.forms import CoordinatesFromAddressForm
from artist.models import Artist


class CoordinatesFromAddressView(PermissionRequiredMixin, View):

    permission_required = 'artist.add_artist'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        # Validate request
        form = CoordinatesFromAddressForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors)
        address = form.cleaned_data['address']

        # Return lat/lon for address
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        return JsonResponse({
            'latitude': float("{0:.4f}".format(location.latitude)),
            'longitude': float("{0:.4f}".format(location.longitude)),
        })


class ArtistListView(ListView):

    template_name = 'artist/artist_list.html'
    context_object_name = 'artists'

    def genre(self, artist):
        artist.genre = ', '.join(artist.genres.all().values_list('name', flat=True))
        return artist.genre

    def percentage_funded(self, artist):
        campaign = artist.latest_campaign()
        if campaign:
            funded = campaign.percentage_funded()
            artist.funded = funded
            return funded

    def location(self, artist):
        user_lat = self.request.GET.get('lat', 0)
        user_lon = self.request.GET.get('lon', 0)
        user_location = (user_lat, user_lon,)
        artist_location = (artist.lat, artist.lon,)
        return distance(user_location, artist_location)

    def dispatch(self, request, *args, **kwargs):
        self.order_by = request.GET.get('sort', 'date')
        return super(ArtistListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['order_by'] = self.order_by
        return context

    def get_queryset(self):
        artists = Artist.objects.all()

        order_by_name = self.order_by
        if order_by_name == 'genre':
            ordered_artists = sorted(artists, key=self.genre)
        elif order_by_name == 'funded':
            ordered_artists = sorted(artists, key=self.percentage_funded, reverse=True)
        elif order_by_name == 'location':
            ordered_artists = sorted(artists, key=self.location)
        else:
            ordered_artists = artists.order_by('id')

        return ordered_artists


class ArtistDetailView(DetailView):

    model = Artist
    context_object_name = 'artist'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(*args, **kwargs)
        context['PINAX_STRIPE_PUBLIC_KEY'] = settings.PINAX_STRIPE_PUBLIC_KEY
        context['PERDIEM_FEE'] = settings.PERDIEM_FEE

        campaign = context['artist'].latest_campaign()
        if campaign:
            context['campaign'] = campaign
            context['investors'] = campaign.investors()

        return context

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

from geopy.geocoders import Nominatim

from artist.forms import CoordinatesFromAddressForm
from artist.models import Genre, Artist


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

    ORDER_BY_NAME = {
        'recent': 'Recently Added',
        'funded': '% Funded',
    }

    def percentage_funded(self, artist):
        campaign = artist.latest_campaign()
        if campaign:
            funded = campaign.percentage_funded()
            artist.funded = funded
            return funded

    def dispatch(self, request, *args, **kwargs):
        # Filtering
        self.active_genre = request.GET.get('genre', 'All')
        self.lat = request.GET.get('lat')
        self.lon = request.GET.get('lon')
        self.distance = request.GET.get('distance')

        # Sorting
        order_by_slug = request.GET.get('sort')
        if order_by_slug not in self.ORDER_BY_NAME:
            order_by_slug = 'recent'
        self.order_by = {
            'slug': order_by_slug,
            'name': self.ORDER_BY_NAME[order_by_slug],
        }
        return super(ArtistListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        sort_options = [{'slug': s, 'name': n,} for s, n in self.ORDER_BY_NAME.iteritems()]
        context.update({
            'genres': Genre.objects.all().order_by('name').values_list('name', flat=True),
            'active_genre': self.active_genre,
            'lat': self.lat,
            'lon': self.lon,
            'distance': self.distance,
            'sort_options': sorted(sort_options, key=lambda o: o['name']),
            'order_by': self.order_by,
        })
        return context

    def get_queryset(self):
        artists = Artist.objects.all()

        # Filter by genre
        if self.active_genre != 'All':
            artists = artists.filter(genres__name=self.active_genre)

        # Filter by location
        if self.lat and self.lon and self.distance:
            artists = artists.filter_by_location(distance=int(self.distance), lat=self.lat, lon=self.lon)

        # Sorting
        order_by_name = self.order_by['slug']
        if order_by_name == 'funded':
            ordered_artists = sorted(artists, key=self.percentage_funded, reverse=True)
        else:
            ordered_artists = artists.order_by('-id')

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

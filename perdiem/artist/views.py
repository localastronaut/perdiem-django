"""
:Created: 19 March 2016
:Author: Lucas Connors

"""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View, DetailView
from django.views.generic.list import ListView
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

    model = Artist
    context_object_name = 'artists'


class ArtistDetailView(DetailView):

    model = Artist
    context_object_name = 'artist'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(*args, **kwargs)
        campaigns = context['artist'].campaign_set.all().order_by('-start_datetime')
        if campaigns:
            context['campaign'] = campaigns[0]
        return context

$(document).ready(function() {
    'use strict'

    // Get user's location when sorting by location
    function get_order_by_location(position) {
        var lat, lon;
        if (position && position.coords) {
            lat = position.coords.latitude;
            lon = position.coords.longitude;
        }
        var url = '?genre=' + active_genre + '&sort=location';
        if (lat) url += '&lat=' + lat;
        if (lon) url += '&lon=' + lon;
        window.location.href = url;
    }

    $('button#location').click(function() {
        if (navigator.geolocation) {
            $('.getting-location').show();
            navigator.geolocation.getCurrentPosition(get_order_by_location, get_order_by_location);
        } else {
            get_order_by_location(null);
        }
    });
});

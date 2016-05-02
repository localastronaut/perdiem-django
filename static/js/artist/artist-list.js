$(document).ready(function() {
    'use strict'

    // Close location dropdown pane when clicking away
    $(document).click(function() {
        $('#location-dropdown').foundation('close');
    });
    $('.dropdown a').click(function() {
        $('#location-dropdown').foundation('close');
    });
    $('.dropdown-pane .slider').click(function(e) {
        e.stopPropagation();
    });
    $('button#location-dropdown-button').click(function(e) {
        $('#location-dropdown').foundation('open');
        e.stopPropagation();
    });

    // Filter by user's location
    function get_order_by_location(position) {
        var lat, lon;
        if (position && position.coords) {
            lat = position.coords.latitude;
            lon = position.coords.longitude;
        }
        var url = '?genre=' + active_genre + '&distance=' + $('.dropdown-pane input').val();
        if (lat) url += '&lat=' + lat;
        if (lon) url += '&lon=' + lon;
        url += '&sort=' + order_by;
        window.location.href = url;
    }
    $('.dropdown-pane button#location-update-button').click(function() {
        if (navigator.geolocation) {
            $('.getting-location').show();
            navigator.geolocation.getCurrentPosition(get_order_by_location, get_order_by_location);
        } else {
            get_order_by_location(null);
        }
    });

    // Reset location
    $('.dropdown-pane button#location-reset-button').click(function() {
        window.location.href = '?genre=' + active_genre + '&sort=' + order_by;
    });
});

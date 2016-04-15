$(document).ready(function() {
    'use strict'

    // CSRF
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#invest-button').click(function(e) {
        stripe_handler.open({
            name: 'PerDiem',
            description: 'Invest in ' + artist_name,
            amount: share_value_cents
        });
        e.preventDefault();
    });

    $(window).on('popstate', function() {
        handler.close();
    });
});

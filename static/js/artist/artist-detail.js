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
        var subtotal = 1 * share_value_cents;
        var perdiem_fee = 100; // $1
        var total = (perdiem_fee + subtotal) * 1.029 + 30; // Stripe 2.9% + $0.30 fee
        stripe_handler.open({
            name: 'PerDiem',
            description: 'Invest in ' + artist_name,
            amount: Math.ceil(total)
        });
        e.preventDefault();
    });

    $(window).on('popstate', function() {
        handler.close();
    });
});

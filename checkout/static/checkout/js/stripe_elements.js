/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// set-up stripe by creating a variable using the stripe public key
var stripe = Stripe(stripePublicKey);
// use stripe to create an instance of elements
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// use elements to create a card element
var card = elements.create('card', {style: style});

// mount the card element to the div
card.mount('#card-element');

// Handle realtime validation on the card element
// Adding a change event to th card to check for any errors 
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    // if so, we'll display error in the card errors div on the checkout page
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // prevent default action of 'POST'
    ev.preventDefault();
    // disable the card element and submit button to prevent multiple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);

    // loading spinner and form fade
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    /* For cached checkout data: */
    // Get the boolean value of the save info checkbox by just looking at its checked value
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    /* Create an object to pass this information to the view and also pass
    the client secret for the payment intent */
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    // Create a new variable for ther URL
    var url = '/checkout/cache_checkout_data/';
    // Finally post this data to the view using jquery post method
    $.post(url, postData).done(function () {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        /* call the confirm card payment method & 
        provide the card to stripe then execute the function */
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                /* re-enable the card element and 
                submit button so user can amend card details */ 
                $(errorDiv).html(html);

                // loading spinner and form fade
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);

                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);

            /* if the status of the payment intent comes 
            back as successfull we then submit the form */
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    })
});

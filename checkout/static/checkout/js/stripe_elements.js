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
        `
        $(errorDiv).html(html);
    } else {
        errorDiv.text = '';
    }
});
// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // prevent default action of 'POST'
    ev.preventDefault();
    // disable to card element and submit button to prevent multiple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    /* call the confirm card payment method & 
    provide the card to stripe then execute the function */
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
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
});




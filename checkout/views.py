from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    # getting the bag from the user session
    bag = request.session.get('bag', {})
    # if nothing is in the bag, produce error message
    if not bag:
        messages.error(request, "Sorry, there's nothing in your shopping bag at the moment")
        return redirect(reverse('products'))

    # creating an instance of your order form, empty at present
    order_form = OrderForm()
    # create the template
    template = 'checkout/checkout.html'

    # context containing order form
    context = {
        'order_form': order_form,
        # Stripe
        'stripe_public_key': 'pk_test_51JYUgnCCIKFmYvsacuVq6enUbna18SqsLGWNoZdP5k7S9mZ04Uxrq09mJu9BxHNp2Fz8q9i6Hjc5RWGpI1gmMOQN00Viz82h9P',
        'client_secret': 'test client secret',
    }
    # and finally render it all out
    return render(request, template, context)

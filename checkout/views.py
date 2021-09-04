from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


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
    }
    # and finally render it all out
    return render(request, template, context)

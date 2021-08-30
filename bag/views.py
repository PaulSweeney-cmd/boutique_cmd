from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view that renders the shopping bag contents """

    return render(request, 'bag/bag.html')


# submit the form to the view including the product id and quantity
def add_to_bag(request, item_id):
    """ A view to render the bag contents page """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # geting the bag variable if it exists -
    # in the session or create if it doesnt
    bag = request.session.get('bag', {})

    # adding an if statement to check whether a product-
    # with sizes is being added
    if size:
        # if the item is already in the bag
        if item_id in list(bag.keys()):
            # checking if another item of the same id and same size exists
            if size in bag[item_id]['items_by_size'].keys():
                # if so then increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # otherwise just se it equal to the quantity
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # update the quantity if it already exsists
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        # add item to the bag
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag!')

    # overwrite the variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ A view to adjust the quantity of the
        product to the specified amount """

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # geting the bag variable if it exists -
    # in the session or create if it doesnt
    bag = request.session.get('bag', {})

    if size:
        # if the quantity in the bag is more than zero,
        # set the items quantity accordingly
        if quantity > 0:
            # if there is a size, you drill in to the items by size dictionary-
            # find the size and either set its quantity-
            # to update number or remove if zero
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    # overwrite the variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)

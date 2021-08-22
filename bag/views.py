from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """ A view that renders the shopping bag contents """

    return render(request, 'bag/bag.html')


# submit the form to the view including the product id and quantity
def add_to_bag(request, item_id):
    """ A view to render the bag contents page """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # geting the bag variable if it exists -
    # in the session or create if it doesnt
    bag = request.session.get('bag', {})
    # update the quantity if it already exsists
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    # add item to the bag
    else:
        bag[item_id] = quantity
    # overwrite the variable in the session with the updated version
    request.session['bag'] = bag
    return redirect(redirect_url)

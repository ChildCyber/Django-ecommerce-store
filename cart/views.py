from django.http import HttpResponseRedirect
from django.shortcuts import render

from cart import carts
from checkout import checkouts


# Create your views here.
def show_cart(request, template_name="cart/cart_new.html"):
    if request.method == 'POST':
        post_data = request.POST.copy()
        if post_data['submit'] == 'Remove':
            carts.remove_from_cart(request)
        if post_data['submit'] == 'Update':
            carts.update_cart(request)
        if post_data['submit'] == 'Checkout':
            checkout_url = checkouts.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items = carts.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = carts.cart_subtotal(request)

    return render(request, template_name, locals())

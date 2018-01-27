# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts import profile
from cart import carts
from checkout import checkouts
from checkout.forms import CheckoutForm
from checkout.models import Order, OrderItem


# Create your views here.
def show_checkout(request, template_name='checkout/checkout.html'):
    """
    checkout form page to collect user shipping and billing information
    """
    if carts.is_empty(request):
        cart_url = urlresolvers.reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = CheckoutForm(post_data)
        if form.is_valid():
            response = checkouts.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('checkout:checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = u'Correct the errors below'
    else:
        if request.user.is_authenticated():
            user_profile = profile.retrieve(request)
            form = CheckoutForm(instance=user_profile)
        else:
            form = CheckoutForm()

    page_title = 'Checkout'

    return render(request, template_name, locals())


def receipt(request, template_name='checkout/receipt.html'):
    """
    page displayed with order information after an order has been placed successfully
    """
    order_number = request.session.get('order_number', '')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
    else:
        cart_url = urlresolvers.reverse('cart:show_cart')
        return HttpResponseRedirect(cart_url)

    return render(request, template_name, locals())

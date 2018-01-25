# -*- coding: utf-8 -*-
from checkout import google_checkout


def get_checkout_url(request):
    """
    returns the URL from the checkout module for cart
    """
    # use this for Google Checkout API:
    return google_checkout.get_checkout_url(request)

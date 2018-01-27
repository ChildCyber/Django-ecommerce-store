# -*- coding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def register(request, template_name="registration/register.html"):
    """
    view displaying customer registration form
    """
    pass


def my_account(request, template_name="registration/my_account.html"):
    """
    page displaying customer account information, past order list and account options
    """
    pass


def order_details(request, order_id, template_name="registration/order_details.html"):
    """
    displays the details of a past customer order; order details can only be loaded by the same
    user to whom the order instance belongs.
    """
    pass


def order_info(request, template_name="registration/order_info.html"):
    """
    page containing a form that allows a customer to edit their billing and shipping information that
    will be displayed in the order form next time they are logged in and go to check out
    """
    pass


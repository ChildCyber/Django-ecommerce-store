# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from accounts import profile
from accounts.forms import RegistrationForm, UserProfileForm
from checkout.models import Order, OrderItem


# Create your views here.
def register(request, template_name="registration/register.html"):
    """
    view displaying customer registration form
    """
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = RegistrationForm(post_data)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)  # new
            user.email = post_data.get('email', '')  # new
            user.save()  # new
            un = post_data.get('username', '')
            pw = post_data.get('password1', '')
            from django.contrib.auth import login, authenticate
            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('accounts:my_account')
                return HttpResponseRedirect(url)
    else:
        form = RegistrationForm()
    page_title = 'User Registration'

    return render(request, template_name, locals())


@login_required
def my_account(request, template_name="registration/my_account.html"):
    """
    page displaying customer account information, past order list and account options
    """
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username

    return render(request, template_name, locals())


@login_required
def order_details(request, order_id, template_name="registration/order_details.html"):
    """
    displays the details of a past customer order; order details can only be loaded by the same
    user to whom the order instance belongs.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)

    return render(request, template_name, locals())


@login_required
def order_info(request, template_name="registration/order_info.html"):
    """
    page containing a form that allows a customer to edit their billing and shipping information that
    will be displayed in the order form next time they are logged in and go to check out
    """
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = UserProfileForm(post_data)
        if form.is_valid():
            profile.set(request)
            url = urlresolvers.reverse('accounts:my_account')
            return HttpResponseRedirect(url)
    else:
        user_profile = profile.retrieve(request)
        form = UserProfileForm(instance=user_profile)
    page_title = 'Edit Order Information'

    return render(request, template_name, locals())

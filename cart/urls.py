# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.show_cart, {'template_name': 'cart/cart.html'}, name='show_cart'),
]

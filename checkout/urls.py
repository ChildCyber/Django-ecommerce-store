# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.show_checkout, {'template_name': 'checkout/checkout.html'}, 'checkout'),
    url(r'^receipt/$', views.receipt, {'template_name': 'checkout/receipt.html'}, 'checkout_receipt'),
]

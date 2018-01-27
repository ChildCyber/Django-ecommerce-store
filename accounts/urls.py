# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^register/$', views.register, {'template_name': 'registration/register.html'}, name='register'),
    url(r'^my_account/$', views.my_account, {'template_name': 'registration/register.html'}, name='my_account'),
    url(r'^order_info/$', views.order_info, {'template_name': 'registration/order_info.html'}, name='order_info'),
    url(r'^order_details/(?P<order_id>[-\w]+)/$', views.order_details,
        {'template_name': 'registration/order_details.html'}, name='order_details'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout')
]

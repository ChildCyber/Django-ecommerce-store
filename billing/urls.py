# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_card/$', views.add_card, name='add_card'),
]

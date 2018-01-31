# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import SITEMAPS

urlpatterns = [
    url(r'^robots\.txt$', views.robots, name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': SITEMAPS}),
]

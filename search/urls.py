# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^results/$', views.results, {'template_name': 'search/results.html'}, name='search_results'),
]

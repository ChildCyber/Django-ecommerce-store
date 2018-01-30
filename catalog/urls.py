# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from catalog import views

urlpatterns = [
    url(r'^$', views.index, {'template_name': 'catalog/index.html'}, name='catalog_home'),
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, {'template_name': 'catalog/category.html'},
        name='catalog_category'),
    url(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, {'template_name': 'catalog/product.html'},
        name='catalog_product'),
    url(r'^review/product/add/$', csrf_exempt(views.add_review), name='add_review'),
    url(r'^tag/product/add/$', csrf_exempt(views.add_tag), name='add_tag'),
    url(r'^tag_cloud/$', views.tag_cloud,  {'template_name': 'catalog/tag_cloud.html'}, name='tag_cloud'),
    url(r'^tag/(?P<tag>[-\w]+)/$', views.tag,  {'template_name': 'catalog/tag.html'}, name='tag'),
]

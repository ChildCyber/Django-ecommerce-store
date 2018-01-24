# -*- coding: utf-8 -*-
from django.template import Library

from catalog.models import Category
from cart import carts

register = Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = carts.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.objects.filter(is_active=True)
    return {
            'active_categories': active_categories,
            'request_path': request_path,
            }
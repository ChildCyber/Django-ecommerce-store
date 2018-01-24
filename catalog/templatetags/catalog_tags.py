# -*- coding: utf-8 -*-
from django.template import Library

from cart import carts

register = Library()


@register.inclusion_tag("tags/cart_box.html")
def cart_box(request):
    cart_item_count = carts.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count}

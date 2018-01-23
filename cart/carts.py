# -*- coding: utf-8 -*-
import decimal
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Max
from django.shortcuts import get_object_or_404

from cart.models import CartItem
from catalog.models import Product

CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """
    从session中获取当前用户cart id，如果为空，设置新的cart id

    """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """
    生成cart id
    """
    cart_id_lst = []
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id_lst.append(characters[random.randint(0, len(characters) - 1)])
    return ''.join(cart_id_lst)


def get_cart_items(request):
    """
    返回当前用户购物车中所有商品
    """
    return CartItem.objects.filter(cart_id=_cart_id(request))


def add_to_cart(request):
    """
    商品添加进购物车
    """
    post_data = request.POST.copy()
    # get product slug from post data, return blank if empty
    product_slug = post_data.get('product_slug', '')
    # get quantity added, return 1 if empty
    quantity = post_data.get('quantity', 1)
    # fetch the product or return a missing page error
    p = get_object_or_404(Product, slug=product_slug)
    # get products in cart
    cart_products = get_cart_items(request)
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == p.id:
            # update the quantity if found
            cart_item.augment_quantity(quantity)
            product_in_cart = True
    if not product_in_cart:
        # create and save a new cart item
        ci = CartItem()
        ci.product = p
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


# update quantity for single item
def update_cart(request):
    """
    更新购物车，添加商品

    """
    post_data = request.POST.copy()
    item_id = post_data['item_id']
    quantity = post_data['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


# remove a single item from cart
def remove_from_cart(request):
    """
    删除购物车中商品
    """
    post_data = request.POST.copy()
    item_id = post_data['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):
    """
    购物车商品总价
    """
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total


# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
    """
    购物车商品数量
    """
    return get_cart_items(request).count()


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    """
    清空购物车
    """
    user_cart = get_cart_items(request)
    user_cart.delete()


def remove_old_cart_items():
    """
    1. calculate date of 90 days ago (or session lifespan)
    2. create a list of cart IDs that haven't been modified
    3. delete those CartItem instances

    """
    print "Removing old carts"
    remove_before = datetime.now() + timedelta(days=-settings.SESSION_COOKIE_DAYS)
    cart_ids = []
    old_items = CartItem.objects.values('cart_id').annotate(last_change=Max('date_added')).filter(
            last_change__lt=remove_before).order_by()
    for item in old_items:
        cart_ids.append(item['cart_id'])
    to_remove = CartItem.objects.filter(cart_id__in=cart_ids)
    to_remove.delete()
    print str(len(cart_ids)) + " carts were removed"

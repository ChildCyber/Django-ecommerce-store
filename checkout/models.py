# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from catalog.models import Product


# Create your models here.
class BaseOrderInfo(models.Model):
    """
    base class for storing customer order information
    """

    class Meta:
        abstract = True

    # contact info
    email = models.EmailField(_(u'邮件'), max_length=50)
    phone = models.CharField(_(u'电话'), max_length=20)

    # shipping information
    shipping_name = models.CharField(_(u'送货名'), max_length=50)
    shipping_address_1 = models.CharField(_(u'送货地址1'), max_length=50)
    shipping_address_2 = models.CharField(_(u'送货地址2'), max_length=50, blank=True)
    shipping_city = models.CharField(_(u'送货城市'), max_length=50)
    shipping_state = models.CharField(_(u'送货省'), max_length=2)
    shipping_country = models.CharField(_(u'送货国家'), max_length=50)
    shipping_zip = models.CharField(_(u'邮编'), max_length=10)

    # billing information
    billing_name = models.CharField(_(u'账单名'), max_length=50)
    billing_address_1 = models.CharField(_(u'账单地址1'), max_length=50)
    billing_address_2 = models.CharField(_(u'账单地址2'), max_length=50, blank=True)
    billing_city = models.CharField(_(u'账单城市'), max_length=50)
    billing_state = models.CharField(_(u'账单省'), max_length=2)
    billing_country = models.CharField(_(u'账单国家'), max_length=50)
    billing_zip = models.CharField(_(u'账单邮编'), max_length=10)


class Order(BaseOrderInfo):
    """
    model class for storing a customer order instance
    """
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (CANCELLED, 'Cancelled'),)
    # order info
    date = models.DateTimeField(_(u'日期'), auto_now_add=True)
    status = models.IntegerField(_(u'订单状态'), choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.GenericIPAddressField(_(u'IP'), )
    last_updated = models.DateTimeField(_(u'上次更新时间'), auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(_(u'单号'), max_length=20)

    def __unicode__(self):
        return u'Order #' + str(self.id)

    @property
    def total(self):
        total = decimal.Decimal('0.00')
        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    def get_absolute_url(self):
        return reverse('accounts:order_details', {'order_id': self.id})


class OrderItem(models.Model):
    """
    model class for storing each Product instance purchased in each order
    """
    product = models.ForeignKey('catalog.Product')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey('checkout.Order')

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def get_absolute_url(self):
        return self.product.get_absolute_url()

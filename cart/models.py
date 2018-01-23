# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CartItem(models.Model):
    cart_id = models.CharField(_(u'购物车ID'), max_length=50)
    date_added = models.DateField(_(u'添加时间'), auto_now_add=True)
    quantity = models.IntegerField(_(u'数量'), default=1)
    product = models.ForeignKey('catalog.Product')

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added', ]

    def total(self):
        return self.quantity * self.product.price

    def name(self):
        return self.product.name

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        self.quantity = models.F('quantity') + int(quantity)
        self.save()

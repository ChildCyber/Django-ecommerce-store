# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class PageView(models.Model):
    """
    model class for tracking the pages that a customer views
    """
    class Meta:
        abstract = True

    date = models.DateTimeField(_(u'创建时间'), auto_now=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True)
    # 用于追踪每个用户，存储在session中
    tracking_id = models.CharField(_(u'tracking id'), max_length=50, default='', db_index=True)


class ProductView(PageView):
    """
    tracks product pages that customer views
    """
    product = models.ForeignKey('catalog.Product')

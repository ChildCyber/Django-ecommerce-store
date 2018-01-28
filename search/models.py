# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class SearchTerm(models.Model):
    """
    记录每次内部搜索的内容
    """
    q = models.CharField(_(u'搜索内容'), max_length=50)
    search_date = models.DateTimeField(_(u'搜索时间'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_(u'IP地址'), )
    user = models.ForeignKey(User, null=True)
    # 对应stats.PageView中的tracking_id
    tracking_id = models.CharField(_(u'tracking id'), max_length=50, default='')

    def __unicode__(self):
        return self.q

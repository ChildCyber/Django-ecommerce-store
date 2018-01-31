# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Card(models.Model):
    data = models.CharField(_(u'信用卡信息'), max_length=500)
    user = models.ForeignKey(User)
    num = models.CharField(_(u'卡号'), max_length=4)

    @property
    def display_number(self):
        return u'xxxxxxx-' + unicode(self.num)

    def __unicode__(self):
        return unicode(self.user.username) + ' - ' + self.display_number

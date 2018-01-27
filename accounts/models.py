from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from checkout.models import BaseOrderInfo


# Create your models here.
class UserProfile(BaseOrderInfo):
    """
    stores customer order information used with the last order placed; can be attached to the checkout order form
    as a convenience to registered customers who have placed an order in the past.
    """
    user = models.ForeignKey(User)

    def __unicode__(self):
        return 'User Profile for: ' + self.user.username

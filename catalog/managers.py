# -*- coding: utf-8 -*-
from django.db import models


class ActiveCategoryManager(models.Manager):
    """
    Manager class to return only those categories where each instance is active
    """

    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)

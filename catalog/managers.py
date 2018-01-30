# -*- coding: utf-8 -*-
from django.db import models


class ActiveCategoryManager(models.Manager):
    """
    Manager class to return only those categories where each instance is active
    """

    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class ActiveProductManager(models.Manager):
    """
    Manager class to return only those products where each instance is active
    """

    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager):
    """
    Manager class to return only those products where each instance is featured
    """

    def get_query_set(self):
        return super(FeaturedProductManager, self).get_query_set().filter(is_active=True).filter(is_featured=True)


class ActiveProductReviewManager(models.Manager):
    """
    Manager class to return only those product reviews where each instance is approved
    """

    def all(self):
        return super(ActiveProductReviewManager, self).all().filter(is_approved=True)

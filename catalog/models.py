# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from catalog.managers import ActiveCategoryManager


# Create your models here.
class Category(models.Model):
    """
    商品类别
    """
    name = models.CharField(_(u'类别名称'), max_length=50)
    slug = models.SlugField(_(u'slug'), max_length=50, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    description = models.TextField(_(u'类别描述'))
    is_active = models.BooleanField(_(u'状态'), default=True)
    meta_keywords = models.CharField(_(u'SEO关键字'), max_length=50,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField(_(u'SEO描述'), max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateField(_(u'创建时间'), auto_now_add=True)
    updated_at = models.DateField(_(u'更新时间'), auto_now=True)

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at', ]
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:catalog_category', kwargs={"category_slug": self.slug})


class Product(models.Model):
    """
    商品
    """
    objects = models.Manager()
    active = ActiveCategoryManager()

    name = models.CharField(_(u'商品名称'), max_length=255, unique=True)
    slug = models.SlugField(_(u'slug'), max_length=255, unique=True,
                            help_text='Unique value for product page URL, created automatically from name.')
    brand = models.CharField(_(u'品牌名称'), max_length=50)
    sku = models.CharField(_(u'存货量'), max_length=50)
    price = models.DecimalField(_(u'当前价格'), max_digits=9, decimal_places=2)
    old_price = models.DecimalField(_(u'历史价格'), max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(_(u'商品图片大图'), upload_to='images/products/main')
    thumbnail = models.ImageField(_(u'商品图片缩略图'), upload_to='images/products/thumbnails')
    image_caption = models.CharField(_(u'商品图片标题'), max_length=200)
    is_active = models.BooleanField(_(u'状态'), default=True)
    is_bestseller = models.BooleanField(_(u'畅销商品'),  default=False)
    is_featured = models.BooleanField(_(u'特色商品'), default=False)
    quantity = models.IntegerField(_(u'数量'))
    description = models.TextField(_(u'描述'))
    meta_keywords = models.CharField(_(u'SEO关键字'), max_length=50,
                                     help_text='Comma-delimited set of SEO keywords for keywords meta tag')
    meta_description = models.CharField(_(u'SEO描述'), max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateField(_(u'创建时间'), auto_now_add=True)
    updated_at = models.DateField(_(u'更新时间'), auto_now=True)
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at', ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:catalog_product', kwargs={"product_slug": self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    # user recommendation part
    def cross_sells(self):
        """
        gets other Product instances that have been combined with the current instance in past orders. Includes the orders
        that have been placed by anonymous users that haven't registered
        """
        from checkout.models import Order, OrderItem
        orders = Order.objects.filter(orderitem__product=self)
        order_items = OrderItem.objects.filter(order__in=orders).exclude(product=self)
        products = Product.active.filter(orderitem__in=order_items).distinct()
        return products

    # users who purchased this product also bought....
    def cross_sells_user(self):
        """
        gets other Product instances that have been ordered by other registered customers who also ordered the current
        instance. Uses all past orders of each registered customer and not just the order in which the current
        instance was purchased
        """
        from checkout.models import Order, OrderItem
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(order__user__in=users).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

    def cross_sells_hybrid(self):
        """
        gets other Product instances that have been both been combined with the current instance in orders placed by
        unregistered customers, and all products that have ever been ordered by registered customers
        """
        from checkout.models import Order, OrderItem
        from django.db.models import Q
        orders = Order.objects.filter(orderitem__product=self)
        users = User.objects.filter(order__orderitem__product=self)
        items = OrderItem.objects.filter(Q(order__in=orders) |
                                         Q(order__user__in=users)
                                         ).exclude(product=self)
        products = Product.active.filter(orderitem__in=items).distinct()
        return products

# -*- coding: utf-8 -*-
from django import forms

from catalog.models import Product, ProductReview


# Create your forms here.
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']


# 添加购物车表单
class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
            widget=forms.TextInput(attrs={'size': '2', 'value': '1', 'class': 'quantity', 'maxlength': '5'}),
            error_messages={'invalid': 'Please enter a valid quantity.'},
            min_value=1)
    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data


class ProductReviewForm(forms.ModelForm):
    """
    Form class to submit a new ProductReview instance
    """

    class Meta:
        model = ProductReview
        exclude = ('user', 'product', 'is_approved')

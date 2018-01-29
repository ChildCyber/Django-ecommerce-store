from django.shortcuts import get_object_or_404, redirect, render

from cart import carts
from catalog.forms import ProductAddToCartForm
from catalog.models import Category, Product
from stats import stats


# Create your views here.
def index(request, template_name="catalog/index.html"):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    return render(request, template_name, locals())


def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    product = c.product_set.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(request, template_name, context=locals())


def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description

    if request.method == 'POST':
        # add to cart
        post_data = request.POST.copy()
        form = ProductAddToCartForm(request, post_data)
        if form.is_valid():
            # add to cart and redirect to cart page
            carts.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return redirect('cart:show_cart')
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()
    stats.log_product_view(request, p)

    return render(request, template_name, context=locals())

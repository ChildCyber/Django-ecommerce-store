from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import Context
from django.template.loader import get_template

from cart import carts
from catalog.forms import ProductAddToCartForm, ProductReviewForm
from catalog.models import Category, Product, ProductReview
from stats import stats

from tagging.models import Tag, TaggedItem


# Create your views here.
def index(request, template_name="catalog/index.html"):
    search_recs = stats.recommended_from_search(request)
    featured = Product.featured.all()[0:settings.PRODUCTS_PER_ROW]
    recently_viewed = stats.get_recently_viewed(request)
    view_recs = stats.recommended_from_views(request)

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
    # product review
    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()

    return render(request, template_name, context=locals())


@login_required
def add_review(request):
    """
    AJAX view that takes a form POST from a user submitting a new product review;
    requires a valid product slug and args from an instance of ProductReviewForm;
    return a JSON response containing two variables: 'review', which contains
    the rendered template of the product review to update the product page,
    and 'success', a True/False value indicating if the save was successful.
    """
    form = ProductReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        slug = request.POST.get('slug')
        product = Product.active.get(slug=slug)
        review.user = request.user
        review.product = product
        review.save()

        template = "catalog/product_review.html"
        t = get_template(template)
        html = t.render(Context({'review': review}))
        response = {'success': 'True', 'html': html}

    else:
        html = form.errors.as_ul()
        response = {'success': 'False', 'html': html}
    return JsonResponse(response)


@login_required
def add_tag(request):
    """
    AJAX view that takes a form POST containing variables for a new product tag;
    requires a valid product slug and comma-delimited tag list; returns a JSON response
    containing two variables: 'success', indicating the status of save operation, and 'tag',
    which contains rendered HTML of all product pages for updating the product page.
    """
    tags = request.POST.get('tag', '')
    slug = request.POST.get('slug', '')
    if len(tags) > 2:
        p = Product.active.get(slug=slug)
        html = u''
        template = "catalog/tag_link.html"
        t = get_template(template)
        for tag in tags.split():
            tag.strip(',')
            Tag.objects.add_tag(p, tag)
        for tag in p.tags:
            html += t.render(Context({'tag': tag}))
        response = {'success': 'True', 'html': html}
    else:
        response = {'success': 'False'}
    return JsonResponse(response, safe=False)

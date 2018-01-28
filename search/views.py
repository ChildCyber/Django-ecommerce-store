from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import render

from ecomstore import settings
from search import searchs


# Create your views here.
def results(request, template_name="search/results.html"):
    """
    template for displaying settings.PRODUCTS_PER_PAGE paginated product results
    """
    # get current search phrase
    q = request.GET.get('q', '')

    # get current page number. Set to 1 is missing or invalid
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    matching = searchs.products(q).get('products', [])
    # generate the paginator object
    paginator = Paginator(matching,
                          settings.PRODUCTS_PER_PAGE)
    try:
        results = paginator.page(page)
    except (InvalidPage, EmptyPage):
        results = paginator.page(1)

    searchs.store(request, q)

    page_title = 'Search Results for: ' + q
    return render(request, template_name, locals())

# -*- coding: utf-8 -*-
import base64
import os

from django.conf import settings

from search.models import SearchTerm


def tracking_id(request):
    """
    unique ID to determine what pages a customer has viewed
    """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']


def recommended_from_search(request):
    """
    get the common words from the stored searches
    """
    common_words = frequent_search_words(request)
    from search import searchs
    matching = []
    for word in common_words:
        results = searchs.products(word).get('products', [])
        for r in results:
            if len(matching) < settings.PRODUCTS_PER_ROW and r not in matching:
                matching.append(r)
    return matching


def frequent_search_words(request):
    """
    gets the three most common search words from the last 10 searches the current customer has entered
    """
    # get the ten most recent searches from the database.
    searches = SearchTerm.objects.filter(tracking_id=tracking_id(request)).values('q').order_by('-search_date')[0:10]
    # join all of the searches together into a single string.
    search_string = ' '.join([search['q'] for search in searches])
    # return the top three most common words in the searches
    return sort_words_by_frequency(search_string)[0:3]


def sort_words_by_frequency(some_string):
    """
    takes a single string of space-delimited word and returns a list of words they contain from most to least frequent
    """
    # convert the string to a python list
    words = some_string.split()
    # assign a rank to each word based on frequency
    ranked_words = [[word, words.count(word)] for word in set(words)]
    # sort the words based on descending frequency
    sorted_words = sorted(ranked_words, key=lambda word: -word[1])
    # return the list of words, most frequent first
    return [p[0] for p in sorted_words]

import os

from django.conf import settings
from django.shortcuts import HttpResponse

ROBOTS_PATH = os.path.join(settings.BASE_DIR, 'marketing/robots.txt')


# Create your views here.
def robots(request):
    """
    view for robots.txt file
    """
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')

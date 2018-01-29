# -*- coding: utf-8 -*-
import base64
import os


def tracking_id(request):
    """
    unique ID to determine what pages a customer has viewed
    """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']

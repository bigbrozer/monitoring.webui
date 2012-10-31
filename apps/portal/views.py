# Std imports
import logging

# Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext


def portal_home(request):
    """
    The home of the portal.
    """
    logger = logging.getLogger('optools.debug.portal_home')

    title = "Home"
    section = dict({'home': 'active'})

    return render_to_response(
        'portal/portal.html',
        locals(),
        context_instance = RequestContext(request)
    )


# Views for app portal

# Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext


def portal_home(request):
    """
    The home of the portal.
    """
    context = {
        'title': "Home",
        'section': {'home': 'active'},
    }

    return render_to_response(
        'portal/portal.html',
        context,
        context_instance = RequestContext(request)
    )


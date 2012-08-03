from django.shortcuts import render_to_response
from django.template import RequestContext

import httpagentparser

def portal_home(request):
    """
    The home of the portal.
    """
    title = "Home"
    section = dict({'home': 'active'})
    old_browser = False

    # Parse user agent and detect old browser
    browser = httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']
    if "internet explorer" in browser['name'].lower() and int(browser['version'].split('.')[0]) < 9:
        old_browser = True

    return render_to_response(
        'portal/portal.html',
        locals(),
        context_instance = RequestContext(request)
    )


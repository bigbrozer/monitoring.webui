"""
Django views for application announce.
"""

# Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# Models imports
from models import Announcement


def show(request):
    """
    Show the currently active announcement.

    Parameters:
        redirect: url where to redirect
    Template:
        announce/announce_show.html
    Context:
        announce (Announcement model)
    """
    try:
        redirect_url = request.GET['redirect']
    except KeyError:
        redirect_url = "/"

    announce = Announcement.objects.get(is_enabled=True)
    return render_to_response(
        "announce/announce_show.html",
        locals(),
        context_instance=RequestContext(request)
    )

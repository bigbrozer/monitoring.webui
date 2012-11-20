"""
Django views for application announce.
"""

# Django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# Models imports
from models import Announcement


def show(request, announce_id=None):
    """
    Show the currently active announcement.

    Arguments:
        announce_id: ID of an existing announcement to show it.
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

    if announce_id:
        announce = Announcement.objects.get(pk=announce_id)
    else:
        announce = Announcement.objects.get(is_enabled=True)

    return render_to_response(
        "announce/announce_show.html",
        locals(),
        context_instance=RequestContext(request)
    )


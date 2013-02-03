"""
Django views for application announce.
"""

# Django imports
from django.shortcuts import render

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
    context = {}

    # Should we redirect user after pressing Continue ?
    context['redirect_url'] = request.GET.get('redirect', '/')

    if announce_id:
        context['announce'] = Announcement.objects.get(pk=announce_id)
    else:
        context['announce'] = Announcement.objects.get(is_enabled=True)

    return render(request, "announce/announce_show.html", context)


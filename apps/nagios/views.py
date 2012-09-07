"""
Django views for application nagios.
"""

# Django imports
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


# View definitions
# ================
#
def get_satellite_list(request, format='json'):
    """
    Return the list of all satellites, format is json by default.
    """
    from django.core import serializers
    from apps.nagios.models import Satellite

    if format not in "csv":
        return HttpResponse(serializers.serialize(format, Satellite.objects.all()))
    else:
        csv = ""
        for sat in Satellite.objects.all():
            csv += "%s;%s;%s;%s\n" % (sat.name, sat.fqdn, sat.alias, sat.live_port)
        return HttpResponse(csv)


def show_kb(request, kb_url):
    """
    Handle the way KB is shown.

    Try to find the first procedure found in ``kb_url``. Redirect to it if found.

    For peoples member of group **kb_manager**, propose to create the procedure if missing. Propose to create the
    procedure also for others levels.

    For others, it says that the procedure is missing and the alert should be part of a Stratos ticket to the relevant
    group.

    :param kb_url: the dokuwiki procedure page of the form ``xxx:xxx:xxx...``.

    Template:
        nagios/procedure.html
    """
    return HttpResponse(kb_url)
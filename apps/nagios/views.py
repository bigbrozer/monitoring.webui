# Nagios app views

# Django imports
from django.http import HttpResponse
from django.core import serializers

# Models imports
from apps.nagios.models import Satellite


# View definitions
# ================
#
def get_satellite_list(request, format='json'):
    """
    Return the list of all satellites, format is json by default.
    """
    if format not in "csv":
        return HttpResponse(serializers.serialize(format, Satellite.objects.all()))
    else:
        csv = ""
        for sat in Satellite.objects.all():
            csv += "%s;%s;%s;%s\n" % (sat.name, sat.fqdn, sat.alias, sat.live_port)
        return HttpResponse(csv)


def find_procedure(request, wiki_url):
    """
    Return the first procedure page based on a Wiki link.

    :param wiki_url: the full dokuwiki URL of the form ``xxx:xxx:xxx``...
    :returns: the first wiki page found.
    """
    pass

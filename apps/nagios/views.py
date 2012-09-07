"""
Django views for application nagios.
"""

# Django imports
from django.http import HttpResponse


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

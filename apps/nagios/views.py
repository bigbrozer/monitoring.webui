# Nagios app views

# Django imports
from django.http import HttpResponse
from django.core import serializers

# Models imports
from apps.nagios.models import Satellite

# Utility
import cjson

# View definitions
# ================
#
# Return the list of all satellites, format is json by default.
def get_satellite_list(request, format='json'):
    if format not in "csv":
    	return HttpResponse(serializers.serialize(format, Satellite.objects.all()))
    else:
        csv = ""
        for sat in Satellite.objects.all():
            csv += "%s;%s;%s;%s\n" % (sat.name, sat.fqdn, sat.alias, sat.live_port)
        return HttpResponse(csv)


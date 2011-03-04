# Nagios app views

# Django imports
from django.http import HttpResponse
from django.core import serializers

# Models imports
from optools.Nagios.models import Satellite

# View definitions
# ================
#
# Return the list of all satellites, format is json by default.
def get_satellite_list(request, format='json'):
	return HttpResponse(serializers.serialize(format, Satellite.objects.all()))

# Nagios app views

# Django imports
from django.http import HttpResponse
from django.core import serializers

# Models imports
from optools.apps.nagios.models import Satellite

# Backend
import optools.backends.livestatus as live

# Utility
import cjson

# View definitions
# ================
#
# Return the list of all satellites, format is json by default.
def get_satellite_list(request, format='json'):
	return HttpResponse(serializers.serialize(format, Satellite.objects.all()))

# Return as JSON the list of hosts that match a string.
def search_hosts(request):
	# Should we search a string or all ? (Limited to 10 results)
	LIMIT = 10
	try:
		match = request.REQUEST['term']
	except KeyError:
		match = ''

	# Connection settings to access satellites using livestatus
	satellite_connect_settings = {}
	for sat in Satellite.objects.all():
		satellite_connect_settings.update(sat.as_live_dict())
	satellites = live.MultiSiteConnection(satellite_connect_settings)

	# Search for hosts
	results = satellites.query("""GET hosts\n\
Columns: name\n\
Limit: 5\n\
Filter: name ~~ %s\n""" % (match))

	found_hosts = sorted([ host.pop() for host in results])[:LIMIT]
	
	return HttpResponse(cjson.encode(found_hosts))

# Nagios app views

# Django imports
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import ListView

# Models imports
from apps.nagios.models import Satellite

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


# Show the list of satellites
class SatelliteListView(ListView):
    context_object_name = "satellite_list"
    model = Satellite

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SatelliteListView, self).get_context_data(**kwargs)
        context['section'] = {'satellites': 'active'}
        context['base_url'] = self.request.build_absolute_uri('/').strip('/')
        return context
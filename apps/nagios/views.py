"""
Django views for application nagios.
"""

# Std imports
import logging
import time

# Django imports
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Models imports
from apps.nagios.models import Satellite, SecurityPort


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

@csrf_exempt
def send_passive(request):
    """
    Web API that uses HTTP POST requests to send passive checks results to Nagios.

    **Note**
        As this is POST data but we have no form, CSRF protection is off for Django using decorator ``@csrf_exempt``.

    You should provides the following POST variables to the URL of the Web API:

    - host
    - service
    - status
    - message

    How to use with **cURL**
    ------------------------

    This example send a WARNING alert to the service CPU of host NAGIOS_DC_SATELLITE_EDC1::

     curl -f \
     -d host=NAGIOS_DC_SATELLITE_EDC1 \
     -d service=CPU \
     -d status=1 \
     -d message="Test TRAP HTTP" \
     http://monitoring-dc.app.corp/optools/nagios/passive/
    """
    # Get the logger for this view
    logger = logging.getLogger('optools.trap')

    logger.info('-------------------------------')
    logger.info('-- Receiving a new HTTP TRAP --')
    logger.info('-------------------------------')
    logger.info('From: %s %s', request.META['REMOTE_HOST'], request.META['REMOTE_ADDR'])
    logger.info('User-Agent: %s', request.META['HTTP_USER_AGENT'])
    logger.debug('Request body: %s', request.body)

    # Livestatus queries
    command_line = 'COMMAND [{timestamp}] PROCESS_SERVICE_CHECK_RESULT;{host};{service};{status};{message}\n'
    query_find_host = 'GET hosts\nColumns: name services\nFilter: name = {host}\n'
    query_find_service = 'GET services\nColumns: description host_name\nFilter: host_name = {host}\nFilter: description = {service}\nAnd: 2\n'

    # Get POST data
    try:
        params = {
            'host': request.POST['host'].upper(),
            'service': request.POST['service'],
            'status': int(request.POST['status']),
            'message': request.POST['message'],
            'timestamp': int(time.time()),
        }
        logger.debug('Cleaned data: %s', params)
    except KeyError:
        logger.exception('Incomplete POST data !')
        return HttpResponse('Incomplete POST data ! Missing key.\n', status=400)
    except ValueError:
        logger.exception('Incorrect value type for data !')
        return HttpResponse('The key \"status\" should be an integer within 0 (OK), 1 (WARNING), 2 (CRITICAL) and 3 (UNKNOWN).\n', status=400)

    # Prepare data to be sent to Nagios
    try:
        satellites = Satellite.live_connect()
        satellites.set_prepend_site(True)
    except Satellite.SatelliteConnectError as e:
        logger.exception('Error connecting on satellites !')
        return HttpResponse('Unable to connect to Nagios.\nError: {}\n'.format(e), status=400)

    # Check if host and service exist in Nagios
    host_dest = satellites.query(query_find_host.format(**params))
    if host_dest:
        # The host is found, check if service exist
        service_dest = satellites.query(query_find_service.format(**params))
        if service_dest:
            sat = service_dest.pop()[0]

            logger.info('Preparing command for Nagios.')
            logger.debug('Command: %s', command_line.format(**params))
            logger.debug('Satellite: %s', sat)

            satellites.command(command_line.format(**params), sitename=sat)
        else:
            # Service not found
            message = 'Service \"{service}\" does not exist on host \"{host}\".\n'.format(**params)
            logger.error(message)
            return HttpResponse(message, status=400)
    else:
        # Host not found
        message = 'The host \"{host}\" does not exist in Nagios.\n'.format(**params)
        logger.error(message)
        return HttpResponse(message, status=400)

    # Everything is OK
    logger.info('HTTP TRAP processed successfully.')
    return HttpResponse()


# Class-based views
class SatelliteListView(ListView):
    """
    Show the list of satellites.
    """
    context_object_name = "systems_list"
    model = Satellite

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SatelliteListView, self).get_context_data(**kwargs)

        # Adding extra context data to the view
        context['section'] = {'systems': 'active'}
        context['base_url'] = self.request.build_absolute_uri('/').strip('/')
        context['ports'] = SecurityPort.objects.all()

        return context

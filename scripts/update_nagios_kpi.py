#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : update_nagios_kpi.py
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Update Nagios KPI (main program)
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

# NOTES
# -----
#
# 1 week == 604800 seconds

import os, sys
import time
from datetime import date

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Importing models
from optools.apps.nagios.models import Satellite
from optools.apps.reporting.models import NagiosKPI

# External backends
import optools.backends.livestatus as live

# Exceptions
from optools.lib.exceptions import NoSatellites

# Utilities functions
def combine_stats_result(result_data):
	'''Combine stats results for all satellites into a big array'''
	limit = len(result_data[0])
	results = [0] * limit
	for i in xrange(limit):
		for data in result_data:
			results[i] += data[i]
	return results

# Connection settings to access satellites using livestatus
satellite_connect_settings = {}
for sat in Satellite.objects.all():
	satellite_connect_settings.update(sat.as_live_dict())

satellites = live.MultiSiteConnection(satellite_connect_settings)
if satellites.dead_sites():
	raise NoSatellites()

satellites = live.MultiSiteConnection(satellite_connect_settings)
#satellites.set_prepend_site(True)

# Today timestamp
today_timestamp = time.time()

# Get the last KPI from database
# Take into account if no KPI are existing in db
try:
	last_kpi = NagiosKPI.objects.order_by('-date')[0]
	log_startfrom = time.mktime(last_kpi.date.timetuple())	# Convert date object to timestamp, used in querying nagios log
except IndexError:
	# If no KPI are existing, start querying log one week before
	log_startfrom = today_timestamp - 604800.

# Query for all critical & warning alerts (including host alerts as critical)
# Results: [Crit, Warn, AckedCrit, AckedWarn]
query_stats_alerts = """GET log\n\
Columns: type state\n\
Filter: time >= {0:.0f}\n\
Filter: class = 3\n\
Filter: state = 1\n\
Filter: state = 2\n\
Or: 2\n\
Stats: type ~ ^HOST\n\
Stats: state = 2\n\
StatsOr: 2\n\
Stats: type ~ ^SERVICE\n\
Stats: state = 1\n\
StatsAnd: 2\n\
Stats: options ~ ACKNOWLEDGEMENT\n\
Stats: state = 2\n\
StatsAnd: 2\n\
Stats: options ~ ACKNOWLEDGEMENT\n\
Stats: state = 1\n\
StatsAnd: 2\n""".format(log_startfrom)

stats_alerts = combine_stats_result(satellites.query(query_stats_alerts))

# Query for current acknowledged alerts
# Results: [AckCrit, AckWarn]
query_current_svc_acknowledged = """GET services\n\
Columns: description state acknowledged\n\
Filter: acknowledged = 1\n\
Filter: state = 2\n\
Filter: state = 1\n\
Or: 2\n\
Stats: state = 2\n\
Stats: state = 1\n"""

# Results: [AckHosts]
query_current_host_acknowledged = """GET hosts\n\
Columns: name state acknowledged\n\
Filter: acknowledged = 1\n\
Stats: state = 1\n\
Stats: state = 2\n\
StatsOr: 2\n"""

current_acknowledged = combine_stats_result(satellites.query(query_current_svc_acknowledged))
current_host_acknowledged = combine_stats_result(satellites.query(query_current_host_acknowledged))
current_acknowledged[0] += current_host_acknowledged.pop()		# Host alerts are considered as critical

# Query for total number of monitored hosts
# Results: [TotalHosts]
query_total_monitored_hosts = """GET hosts\n\
Columns: name\n\
Stats: name !~ \" \"\n"""

total_monitored_hosts = combine_stats_result(satellites.query(query_total_monitored_hosts))

# Query for total number of monitored services
# Results: [TotalServices]
query_total_monitored_services = """GET services\n\
Columns: description\n\
Stats: description !~ \" \"\n"""

total_monitored_services = combine_stats_result(satellites.query(query_total_monitored_services))

# Save KPI in database
kpi = NagiosKPI()
kpi.alert_crit_total = stats_alerts[0]
kpi.alert_warn_total = stats_alerts[1]
kpi.alert_ack_crit_total = stats_alerts[2]
kpi.alert_ack_warn_total = stats_alerts[3]
kpi.alert_ack_crit_current = current_acknowledged[0]
kpi.alert_ack_warn_current = current_acknowledged[1]
kpi.total_hosts = total_monitored_hosts[0]
kpi.total_services = total_monitored_services[0]
kpi.save()


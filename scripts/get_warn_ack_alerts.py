#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : get_warn_ack_alerts.py
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Script that get the number of warning ack alerts in Nagios.
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

import os, sys

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Importing models
from optools.apps.nagios.models import Satellite
from optools.apps.reporting.models import AckStat
import optools.backends.livestatus as live

warn_ack_total = 0
crit_ack_total = 0

# Class that define an alert result
class Alert(object):
	def __init__(self, host, service, state, timestamp):
		self.host = host
		self.service = service
		self.state = state
		self.date = datetime.fromtimestamp(timestamp)

	def __repr__(self):
		return repr((self.host, self.service, self.state, str(self.date)))

# Connection settings to access satellites using livestatus
satellite_connect_settings = {}
for sat in Satellite.objects.all():
	satellite_connect_settings.update(sat.as_live_dict())

satellites = live.MultiSiteConnection(satellite_connect_settings)
if satellites.dead_sites():
	raise Exception('Unable to get data from Nagios satellites !')

# Query all ack alerts
warn_results = satellites.query("""GET services\n\
Stats: state = 1\n\
Filter: acknowledged = 1\n""")

for x in warn_results:
	warn_ack_total += x[0]

crit_results = satellites.query("""GET services\n\
Stats: state = 2\n\
Filter: acknowledged = 1\n""")

for x in crit_results:
	crit_ack_total += x[0]

# Send to database
stat = AckStat(active_ack_warn = warn_ack_total, active_ack_crit = crit_ack_total)
stat.save()


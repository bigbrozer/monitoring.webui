#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : report_top5_old_ack_alerts.py
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Script that report stats about procedure available in Nagios.
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
from datetime import datetime
from operator import attrgetter

# Adding optools project to sys.path
pwd = os.path.abspath(os.path.dirname(__file__))
optools_dir = os.path.split(pwd)[0]
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Importing models
from Nagios.models import Satellite
import backends.livestatus as live

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

# Query all ack alerts
results = satellites.query("""GET services\n\
Columns: host_name description state last_state_change\n\
Filter: acknowledged = 1\n""")

alert_objects = []
for result in results:
	host_name, service, state, timestamp = result
	
	alert = Alert(host_name, service, state, timestamp)
	alert_objects.append(alert)

# Print the oldest top 5 ack alerts
print sorted(alert_objects, key=attrgetter('date'))[0:5]


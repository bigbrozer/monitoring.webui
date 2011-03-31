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

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Importing models
from optools.apps.nagios.models import Satellite
from optools.apps.reporting.models import NagiosKPI

# External backends
import optools.backends.livestatus as live

# Connection settings to access satellites using livestatus
satellite_connect_settings = {}
for sat in Satellite.objects.all():
	satellite_connect_settings.update(sat.as_live_dict())

satellites = live.MultiSiteConnection(satellite_connect_settings)
if satellites.dead_sites():
	raise Exception('Unable to get data from Nagios satellites !')

# Query all warn alerts
results = satellites.query("""GET log\n\
Columns: message\n\
Filter: time >= 1300984164\n\
Filter: state = 1\n\
Filter: options ~ ACKNOWLEDGEMENT\n\
Filter: class = 3\n""")

print results

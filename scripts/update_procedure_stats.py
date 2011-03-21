#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : update_procedure_stats.py
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : List services that does not have a KB procedure and ones that does.
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

import sys, os
import urllib2

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Importing models
from optools.apps.nagios.models import Satellite
from optools.apps.reporting.models import ProcedureStat
import optools.backends.livestatus as live

#csv_export_dir = '/tmp/django/public_html/reports'								# TESTING
csv_export_dir = '/home/django/public_html/reports'								# PRODUCTION
if not os.path.isdir(csv_export_dir):
	os.makedirs(csv_export_dir)

def get_raw_procedure(url):
	# Create an OpenerDirector with support for Basic HTTP Authentication...
	passwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passwd_manager.add_password(None, 'monitoring-dc.app.corp', '9NagiosDC', 'NglP(23M,n')
	auth_handler = urllib2.HTTPBasicAuthHandler(passwd_manager)
	proxy_handler = urllib2.ProxyHandler({})									# Disable automatic proxy detection
	opener = urllib2.build_opener(auth_handler, proxy_handler)
	# ...and install it globally so it can be used with urlopen.
	urllib2.install_opener(opener)
	
	try:
		procedure = urllib2.urlopen(url + '?do=export_raw')
	except urllib2.HTTPError as e:
		raise SystemExit("Error: URL: {0}\nMessage: {1}".format(url, e))
	return procedure.read()

# Connection settings to access satellites using livestatus
satellite_connect_settings = {}
for sat in Satellite.objects.all():
	satellite_connect_settings.update(sat.as_live_dict())

satellites = live.MultiSiteConnection(satellite_connect_settings)
if satellites.dead_sites():
	raise SystemExit('Unable to get data from Nagios satellites !')

# Query satellites
results = satellites.query("""GET services\n\
Columns: host_name description notes_url_expanded contacts\n""")

# Init file to export results as CSV
output_csv = open(os.path.join(csv_export_dir, "services_without_procedure_in_nagios.csv"), "w")
output_csv.write('host_name;service;url\n')

# Check procedures
total_services = len(results)
progress = 1
num_with_proc = 0
num_without_proc = 0
for service_object in results:
	host, service, kb_url, contacts = service_object
	print "Checking procedure: {0}/{1}.".format(progress, total_services)		# DEBUG
	procedure = get_raw_procedure(kb_url)
	if '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0' in procedure:
		num_without_proc += 1
		output_csv.write("{0};{1};{2};{3}\n".format(host, service, kb_url, ','.join(contacts)))
	else:
		num_with_proc += 1
	progress+=1

# Close CSV file
output_csv.close()

# Send results to database
stat = ProcedureStat(num_no_procedure = num_without_proc, num_with_procedure = num_with_proc)
stat.save()


# Nagios Commands

# Utility
from string import Template
from time import time, mktime
from datetime import datetime

# Importing models
from optools.apps.nagios.models import Satellite
import optools.backends.livestatus as live


class BaseCommand(object):
	"""Base class for defining a Nagios Command to be sent to Livestatus socket."""
	
	def __init__(self, host_name):
		# Connection settings to access satellite using livestatus
		self.satellite_connect_settings = {}
		for sat in Satellite.objects.all():
			self.satellite_connect_settings.update(sat.as_live_dict())
		self.satellites = live.MultiSiteConnection(self.satellite_connect_settings)
		
		# Attributes
		self.name = None
		self.template_values = {
			'host_name': host_name,
		}
		self.template_str = None
	
	def send(self):
		timestamp = time()
		message = self.template_str.substitute(self.template_values)
		full_cmd_string = '[{0:.0f}] {1};{2}'.format(
			timestamp,
			self.name,
			self._format_cmd_options(),
		)
		for site in self.satellite_connect_settings.keys():
			self.satellites.command(full_cmd_string, sitename=site)
	
	# Private methods
	def _datestr_to_timestamp(self, date):
		timestamp = mktime(date.timetuple())
		return '{0:.0f}'.format(timestamp)
	
	def _format_cmd_options(self):
		"""Return string with cmd template variable replaced by values provided by users"""
		
		return self.template_str.substitute(self.template_values)
	
	def _get_login_full_name(self, login):
		"""Return the full name of a login name"""
		
		# Establish link to first satellite who is UP
		satellite = None
		for sat_option in self.satellite_connect_settings.values():
			satellite = live.SingleSiteConnection(sat_option['socket'])
			if satellite.socket_state is not 'DOWN':
				break

		# Query contacts from satellite
		results = satellite.query("""GET contacts\n\
Columns: alias\n\
Filter: name = {0}\n\
Limit: 1\n""".format(login))
		
		# If user is not found in Nagios, use login instead of full name for downtime author
		if len(results):
			return results[0][0]
		else:
			return login


#  ____                      _   _                
# |  _ \  _____      ___ __ | |_(_)_ __ ___   ___ 
# | | | |/ _ \ \ /\ / / '_ \| __| | '_ ` _ \ / _ \
# | |_| | (_) \ V  V /| | | | |_| | | | | | |  __/
# |____/ \___/ \_/\_/ |_| |_|\__|_|_| |_| |_|\___|
#                                                 

class BaseScheduleDowntime(BaseCommand):
	"""
	Base class to define a command to schedule a downtime in Nagios.
	
	:param string host_name: name of the host.
	:param datetime start_time: start period.
	:param datetime end_time: end period.
	:param string login: user login (ex. 0besancon).
	:param string description: downtime comment in Nagios.
	"""
	
	def __init__(self, host_name, start_time, end_time, login, description):
		super(BaseScheduleDowntime, self).__init__(host_name)
		
		self.template_values.update({
			'start_time': self._datestr_to_timestamp(start_time),
			'end_time': self._datestr_to_timestamp(end_time),
			'author': self._get_login_full_name(login),
			'description': description,
		})
		self.template_str = Template('$host_name;$start_time;$end_time;1;0;0;$author;$description')


class ScheduleHostDowntime(BaseScheduleDowntime):
	"""
	Define a command to schedule a host downtime in Nagios (service exclusive).
	"""
	
	def __init__(self, host_name, start_time, end_time, login, description):
		super(ScheduleHostDowntime, self).__init__(host_name, start_time, end_time, login, description)
		
		self.name = 'SCHEDULE_HOST_DOWNTIME'


class ScheduleHostSvcDowntime(BaseScheduleDowntime):
	"""
	Define a command to schedule a downtime in Nagios for all services on host (host exclusive).
	"""
	
	def __init__(self, host_name, start_time, end_time, login, description):
		super(ScheduleHostSvcDowntime, self).__init__(host_name, start_time, end_time, login, description)
		
		self.name = 'SCHEDULE_HOST_SVC_DOWNTIME'


class ScheduleFullDowntime(object):
	"""
	Define a command to schedule a host downtime including all services on host in Nagios.
	"""
	
	def __init__(self, host_name, start_time, end_time, login, description):
		self.commands = [
			ScheduleHostDowntime(host_name, start_time, end_time, login, description),
			ScheduleHostSvcDowntime(host_name, start_time, end_time, login, description)
		]
	
	def send(self):
		for cmd in self.commands:
			cmd.send()


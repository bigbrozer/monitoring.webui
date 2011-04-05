# Reporting models

from django.db import models

# Utility
from datetime import datetime

# Nagios KPI model
class NagiosKPI (models.Model):
	date = models.DateTimeField(auto_now_add=False)
	service_with_kb = models.PositiveIntegerField(default=0)
	service_without_kb = models.PositiveIntegerField(default=0)
	alert_warn_total = models.PositiveIntegerField(default=0)
	alert_crit_total = models.PositiveIntegerField(default=0)
	alert_ack_warn_total = models.PositiveIntegerField(default=0)
	alert_ack_crit_total = models.PositiveIntegerField(default=0)
	alert_ack_warn_current = models.PositiveIntegerField(default=0)
	alert_ack_crit_current = models.PositiveIntegerField(default=0)
	total_hosts = models.PositiveIntegerField(default=0)
	total_services = models.PositiveIntegerField(default=0)
	
	def __unicode__(self):
		return u'Nagios KPI ({0})'.format(self.date.strftime('%d-%m-%Y %H:%M:%S'))

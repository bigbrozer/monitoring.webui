# Reporting models

from django.db import models

# Utility
from datetime import date

#===============================================================================
#  ____                                _           _ 
# |  _ \  ___ _ __  _ __ ___  ___ __ _| |_ ___  __| |
# | | | |/ _ \ '_ \| '__/ _ \/ __/ _` | __/ _ \/ _` |
# | |_| |  __/ |_) | | |  __/ (_| (_| | ||  __/ (_| |
# |____/ \___| .__/|_|  \___|\___\__,_|\__\___|\__,_|
#            |_|                                     
#

# Model representing stats about number of active ack alerts per weeks
class AckStat(models.Model):
	date = models.DateField(auto_now_add=True)
	active_ack_warn = models.PositiveIntegerField('Ack Warning alerts')
	active_ack_crit = models.PositiveIntegerField('Ack Critical alerts')
	
	def __unicode__(self):
		return u'Stat for date {0}'.format(self.date)

# Model representing stats about number of procedures
class ProcedureStat(models.Model):
	date = models.DateField(auto_now_add=True, auto_now=True)
	num_no_procedure = models.PositiveIntegerField()
	num_with_procedure = models.PositiveIntegerField()
	
	def __unicode__(self):
		return u'{0} services without and {1} with procedure for date {2}'.format(self.num_no_procedure, self.num_with_procedure, self.date)
#===============================================================================

# Nagios KPI model
class NagiosKPI (models.Model):
	date = models.DateField(auto_now_add=True)
	service_with_kb = models.PositiveIntegerField()
	service_without_kb = models.PositiveIntegerField()
	alert_warn_total = models.PositiveIntegerField()
	alert_crit_total = models.PositiveIntegerField()
	alert_ack_warn_total = models.PositiveIntegerField()
	alert_ack_crit_total = models.PositiveIntegerField()
	alert_ack_warn_current = models.PositiveIntegerField()
	alert_ack_crit_current = models.PositiveIntegerField()
	total_hosts = models.PositiveIntegerField()
	total_services = models.PositiveIntegerField()
	
	def __unicode__(self):
		return u'Nagios KPI ({0})'.format(self.date)

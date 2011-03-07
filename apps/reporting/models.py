# Reporting models

from django.db import models

# Utility
from datetime import date

# Model representing stats about number of active ack alerts per weeks
class AckStat(models.Model):
	date = models.DateField(default=date.today())
	active_ack_warn = models.PositiveIntegerField('Ack Warning alerts')
	active_ack_crit = models.PositiveIntegerField('Ack Critical alerts')
	
	def __unicode__(self):
		return u'Stat for date {0}'.format(self.date)

# Model representing stats about number of procedures
class ProcedureStat(models.Model):
	date = models.DateField(default=date.today())
	num_no_procedure = models.PositiveIntegerField()
	num_with_procedure = models.PositiveIntegerField()
	
	def __unicode__(self):
		return u'{0} services without and {1} with procedure for date {2}'.format(self.num_no_procedure, self.num_with_procedure, self.date)


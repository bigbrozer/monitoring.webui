# Reporting models

from django.db import models

# Model representing stats about number of active ack alerts per weeks
class AckStat(models.Model):
	date = models.DateField()
	active_ack_warn = models.PositiveIntegerField('Ack Warning alerts')
	active_ack_crit = models.PositiveIntegerField('Ack Critical alerts')
	
	def __unicode__(self):
		return u'Stat for date {0}'.format(self.date)

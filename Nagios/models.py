# Nagios app models

from django.db import models
from django.core.exceptions import ValidationError

# Validators
def validate_network_port(value):
    if not 1024 < value < 65536:
        raise ValidationError(u'Port number should be between 1024 - 65536')

# Model representing list of active Nagios satellites
class Satellite(models.Model):
	name = models.CharField(max_length=4, verbose_name='DC Code', help_text='Example for Hagenbach: HGB')
	
	# Network settings
	alias = models.CharField(max_length=25, help_text='Please use following format: nagios.sss.cc.corp')
	fqdn = models.CharField(max_length=30, verbose_name='DNS', help_text='Fully qualified domain name for the satellite')
	
	# Livestatus
	ip_address = models.IPAddressField()
	live_port = models.PositiveIntegerField(
		default=6557,
		validators=[validate_network_port],
		verbose_name='Livestatus port',
		help_text='Port must be between 1024 - 65536'
	)
	nagios_url = models.CharField(
		max_length=10,
		default='/nagios',
		verbose_name='Base URL',
		help_text='Use at your own risk ! Let it be default if you don\'t know what you are doing'
	)
	
	def __unicode__(self):
		return u'{0} ({1})'.format(self.name, self.alias)
	
	def as_live_dict(self, timeout=5):
		'''Return a dict as expected for livestatus.MultiSiteConnection method.'''
		return {self.name: {
			'alias': self.alias,
			'socket': 'tcp:{0}:{1}'.format(self.alias, self.live_port),
			'nagios_url': self.nagios_url,
			'timeout': timeout,
		}}


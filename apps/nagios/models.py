# Nagios app models

from django.db import models
from django.core.exceptions import ValidationError


# Validators
def validate_network_high_port(value):
    if not 1024 < value < 65536:
        raise ValidationError(u'Port number should be between 1024 - 65535')

def validate_network_port(value):
    if not 0 < value < 65536:
        raise ValidationError(u'Port number should be between 1 - 65535')


# Models
class Satellite(models.Model):
    """Model representing list of active Nagios satellites"""
    name = models.CharField(max_length=4, verbose_name='DC Code', help_text='Example for Hagenbach: HGB')

    # Network settings
    alias = models.CharField(max_length=25, help_text='Please use following format: nagios.sss.cc.corp')
    fqdn = models.CharField(max_length=30, verbose_name='DNS', help_text='Fully qualified domain name for the satellite')

    # Livestatus
    ip_address = models.IPAddressField()
    live_port = models.PositiveIntegerField(
        default=6557,
        validators=[validate_network_high_port],
        verbose_name='Livestatus port',
        help_text='Port must be between 1024 - 65536'
    )
    nagios_url = models.CharField(
        max_length=10,
        default='/nagios',
        verbose_name='Base URL',
        help_text='Use at your own risk ! Let it be default if you don\'t know what you are doing'
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.alias)

    def as_live_dict(self, timeout=5):
        """Return a dict as expected for :meth:`livestatus.MultiSiteConnection` method."""
        return {self.name: {
            'alias': self.alias,
            'socket': 'tcp:{0}:{1}'.format(self.ip_address, self.live_port),
            'nagios_url': self.nagios_url,
            'timeout': timeout,
        }}


class SecurityPort(models.Model):
    """
    Store port information needed on Firewalls in order to allow access from Nagios to monitored hosts.
    """
    NETWORK_PROTOCOL = (
        ('ICMP', 'ICMP'),
        ('TCP', 'TCP'),
        ('UDP', 'UDP'),
        ('TCP/UDP', 'TCP/UDP'),
    )

    name = models.CharField(max_length=64, help_text='Port name. eg. SNMP, SSH, etc...')
    description = models.CharField(max_length=128, help_text='Enter a description for this port.')
    begin_port = models.PositiveIntegerField(max_length=5, validators=[validate_network_port], help_text='Enter the begin port number.')
    end_port = models.PositiveIntegerField(max_length=5, validators=[validate_network_port], help_text='Enter the end port number. Keep it empty if none.', null=True, blank=True)
    protocol = models.CharField(max_length=7, choices=NETWORK_PROTOCOL, help_text='Choose the network protocol to use.')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

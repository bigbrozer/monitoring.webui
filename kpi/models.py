"""
django models
"""
from django.db import models
from datetime import timedelta


class KpiNagios(models.Model):
    """
    Stock all the key indicators found in Nagios Database
    """
    date = models.DateTimeField()

    total_host = models.PositiveIntegerField()
    total_services = models.PositiveIntegerField()
    written_procedures = models.PositiveIntegerField()
    missing_procedures = models.PositiveIntegerField()
    linux = models.PositiveIntegerField()
    windows = models.PositiveIntegerField()
    aix = models.PositiveIntegerField()
    total_host.verbose_name = 'Hosts'
    total_services.verbose_name = 'Services'

    def __unicode__(self):
        return str(self.date)

class KpiRedmine(models.Model):
    """
    Stock all the key indicators found in Redmine Database
    """

    date = models.DateTimeField()

    requests_opened = models.PositiveIntegerField('opened')
    requests_closed = models.PositiveIntegerField('closed')
    requests_remained = models.PositiveIntegerField('remained')
    requests_lifetime = models.PositiveIntegerField()
    requests_lifetime_normal = models.PositiveIntegerField()
    requests_lifetime_high = models.PositiveIntegerField()
    requests_lifetime_urgent = models.PositiveIntegerField()


    def lifetime(self):
        """
        return the lifetime global
        """
        return "%s" % timedelta(seconds = self.requests_lifetime)

    def lifetime_normal(self):
        """
        return the lifetime normal
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_normal)

    def lifetime_high(self):
        """
        return the lifetime high
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_high)

    def lifetime_urgent(self):
        """
        return the lifetime urgent
        """
        return "%s" % timedelta(seconds = self.requests_lifetime_urgent)

    lifetime.admin_order_field = 'requests_lifetime'
    lifetime.short_description = 'average lifetime (global)'

    lifetime_normal.admin_order_field = 'requests_lifetime_normal'
    lifetime_normal.short_description = 'average lifetime (normal)'

    lifetime_high.admin_order_field = 'requests_lifetime_high'
    lifetime_high.short_description = 'average lifetime (high)'

    lifetime_urgent.admin_order_field = 'requests_lifetime_urgent'
    lifetime_urgent.short_description = 'average lifetime (urgent)'

    def __unicode__(self):
        return str(self.date)

class NagiosNotifications(models.Model):
    """
    Stock all the key indicators found in the table log of Nagios Database
    """

    host = models.CharField(max_length = 64)
    service = models.CharField(max_length = 128, null = True)
    date = models.DateTimeField(null = True)
    STATE_CHOICES = ((1, 'Warning'),(2, 'Critical'))
    state = models.PositiveIntegerField(choices = STATE_CHOICES)
    acknowledged = models.BooleanField()

    def __unicode__(self):
        return str(self.date)
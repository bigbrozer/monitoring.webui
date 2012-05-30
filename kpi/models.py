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
    alerts_hard_warning = models.PositiveIntegerField()
    alerts_hard_critical = models.PositiveIntegerField()
    alerts_acknowledged_warning = models.PositiveIntegerField()
    alerts_acknowledged_critical = models.PositiveIntegerField()

    def __unicode__(self):
        return str(self.date)
    
class KpiRedmine(models.Model):
    """
    Stock all the key indicators found in Redmine Database
    """

    date = models.DateTimeField()

    requests_opened = models.PositiveIntegerField()
    requests_closed = models.PositiveIntegerField()
    requests_remained = models.PositiveIntegerField()
    requests_lifetime = models.PositiveIntegerField()

    # def requests_lifetime(self):
    #     t = timedelta(seconds=(self.request_lifetime))
    #     return str(t)

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
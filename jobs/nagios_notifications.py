import sys
import os
import calendar


sys.path.insert(0, os.path.dirname(os.path.dirname(sys.argv[0])))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reporting.settings'

from kpi.models import NagiosNotifications

def getLastTime():
    """
    return the last timestamp foud in the database
    return 0 if the database is empty
    """
    try:
        lastDate = NagiosNotifications.objects.order_by('-date')[0].date
        lastTimestamp = calendar.timegm(lastDate.timetuple()) 
    except:
        lastTimestamp = 0

    return lastTimestamp

def request():
    """
    return a dictionnary containing the number of alerts for each state
    """

    alerts_hard_warning = NagiosNotifications.objects.filter(state = 1, acknowledged = False).count()
    alerts_hard_critical = NagiosNotifications.objects.filter(state = 2, acknowledged = False).count()
    alerts_acknowledged_warning = NagiosNotifications.objects.filter(state = 1, acknowledged = True).count()
    alerts_acknowledged_critical = NagiosNotifications.objects.filter(state = 2, acknowledged = True).count()
    result = {
    'alerts_hard_warning': alerts_hard_warning,
    'alerts_hard_critical': alerts_hard_critical,
    'alerts_acknowledged_warning': alerts_acknowledged_warning,
    'alerts_acknowledged_critical': alerts_acknowledged_critical,
    }    
    return result
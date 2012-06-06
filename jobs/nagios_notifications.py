"""
get the notifications from nagios results
"""

import calendar
from datetime import datetime, timedelta
from django.utils.timezone import utc
from kpi.models import NagiosNotifications, KpiNagios

def get_last_time():
    """
    return the last timestamp foud in the database
    return 0 if the database is empty
    """
    try:
        last_date = NagiosNotifications.objects.order_by('-date')[0].date
        last_timestamp = calendar.timegm(last_date.timetuple()) 
    except:
        last_timestamp = 0

    return last_timestamp

def request():
    """
    return a dictionnary containing the number of alerts for each state
    """
    one_day = timedelta(days = 1)
    #frequency of execution
    today = datetime.now(tz=utc)
    today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    yesterday = today - one_day
    try:
        date = KpiNagios.objects.order_by('-date')[0].date.replace(
            hour = 0, minute = 0, second = 0, microsecond = 0)
    except:
        date = today

    if date != yesterday:
        alerts_hard_warning = NagiosNotifications.objects.filter(
            state = 1, acknowledged = False, date__gt = yesterday, 
            date__lt = today).count()
        alerts_hard_critical = NagiosNotifications.objects.filter(
            state = 2, acknowledged = False, date__gt = yesterday, 
            date__lt = today).count()
        alerts_acknowledged_warning = NagiosNotifications.objects.filter(
            state = 1, acknowledged = True, date__gt = yesterday, 
            date__lt = today).count()
        alerts_acknowledged_critical = NagiosNotifications.objects.filter(
            state = 2, acknowledged = True, date__gt = yesterday, 
            date__lt = today).count()
        result = {
        'alerts_hard_warning': alerts_hard_warning,
        'alerts_hard_critical': alerts_hard_critical,
        'alerts_acknowledged_warning': alerts_acknowledged_warning,
        'alerts_acknowledged_critical': alerts_acknowledged_critical,
        }    
        return result
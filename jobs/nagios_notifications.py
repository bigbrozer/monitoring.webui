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

def request(today):
    """
    return a dictionnary containing the number of alerts for each state
    """
    one_day = timedelta(days = 1)
    today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    yesterday = today - one_day

    alerts_hard_warning = result.filter(
        state = 1, acknowledged = False, date__gte = yesterday,
        date__lt = today).count()
    alerts_hard_critical = result.filter(
        state = 2, acknowledged = False, date__gte = yesterday,
        date__lt = today).count()
    alerts_acknowledged_warning = result.filter(
        state = 1, acknowledged = True, date__gte = yesterday,
        date__lt = today).count()
    alerts_acknowledged_critical = result.filter(
        state = 2, acknowledged = True, date__gte = yesterday,
        date__lt = today).count()
    result = {
    'alerts_hard_warning': alerts_hard_warning,
    'alerts_hard_critical': alerts_hard_critical,
    'alerts_acknowledged_warning': alerts_acknowledged_warning,
    'alerts_acknowledged_critical': alerts_acknowledged_critical,
    }
    return result
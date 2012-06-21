"""
get the notifications from nagios results
"""

import calendar
from datetime import datetime, timedelta
from django.utils.timezone import utc
from kpi.models import NagiosNotifications, RecurrentAlerts
from pprint import pprint
from nagios import get_hosts

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

def request(date):
    """
    return a dictionnary containing the number of alerts for each state
    """
    one_day = timedelta(days = 1)
    date = date.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    late = date + one_day
    now = datetime.now(tz=utc)\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    if date >= now:
        return False
    else:
        result = NagiosNotifications.objects.filter(date__gte = date,
            date__lt = late)
        warning = result.filter(
            state = 1, acknowledged = False).count()
        warning_acknowledged = result.filter(
            state = 1, acknowledged = True).count()
        critical = result.filter(
            state = 2, acknowledged = False).count()
        critical_acknowledged = result.filter(
            state = 2, acknowledged = True).count()
        result = {
        'warning': warning,
        'warning_acknowledged': warning_acknowledged,
        'critical': critical,
        'critical_acknowledged': critical_acknowledged,
        }
        return result

def request_recurrent_alerts():
    """
    return a dictionnary containing the number of each alerts the last 31 days
    """
    hosts = get_hosts()
    today = datetime.now(tz=utc)\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    period = timedelta(days = 31)
    first_date = today - period
    if RecurrentAlerts.objects.all().count():
        RecurrentAlerts.objects.all().delete()
    alerts = NagiosNotifications.objects\
        .filter(date__gte = first_date, date__lt = today)\
        .values('host', 'service')
    alerts_list = list(alerts)
    for index, alert in enumerate(alerts_list):
        if not alert['host'] in hosts:
            del alerts_list[index]
    count = {}
    name = ""
    for alert in alerts_list:
        name = "%s;%s" % (alert["host"], alert["service"])
        if count.has_key(str(name)):
            count[str(name)] += 1
        else:
            count[str(name)] = 1
    return count
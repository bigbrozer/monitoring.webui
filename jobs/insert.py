"""
insert data from nagios and redmine to program database
"""
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reporting.settings'

import nagios
import nagios_notifications
import redmine
from kpi.models import NagiosNotifications, CountNotifications
from kpi.models import KpiRedmine, KpiNagios
from django.utils.timezone import utc


def insert():
    """
    Execute the requests in the differents databases, then stock the result in the programm database
    """
    number = 0
    notifications_nagios = get_notifications()
    number += insert_nagios_notifications(notifications_nagios)

    one_day = timedelta(days = 1)
    yesterday = datetime.now(tz=utc).replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)-one_day

    if KpiNagios.objects.all().count() != 0:
        last_date = KpiNagios.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday-one_day


    if last_date != yesterday:
        result_nagios = get_result_nagios()
        number += insert_nagios(result_nagios)

    if CountNotifications.objects.all().count() != 0:
        last_date = CountNotifications.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday-one_day

    if last_date != yesterday:
        number += insert_count_notifications()

    if KpiRedmine.objects.all().count() != 0:
        last_date = KpiRedmine.objects.order_by('-date')[0].date
        last_date = last_date.replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)
    else:
        last_date = yesterday-one_day

    if last_date != yesterday:
        number += insert_redmine()

    return "\n %s lignes ajoutees" % (number)

def get_result_nagios():
    """
    get the results from nagios database
    """
    # return null if a satellite doesn't answer
    result_nagios = nagios.request()
    if not result_nagios:
        raise SystemExit("The connection to a satellite failed")
        # leave the programm by raising an error if a sattelite is "dead"
    return result_nagios
    # return the result if there is no errors

def get_notifications():
    """
    get the last timestamp from the database then use it to get the
    notification from nagios from the last timestamp
    """

    last_timestamp = nagios_notifications.get_last_time()

    notifications_nagios = nagios.request_notifications(last_timestamp)
    return notifications_nagios

def insert_redmine():
    """
    insert redmine kpi into the programm database
    """
    result_redmine = redmine.request()
    number = 0
    for date in result_redmine['requests_opened'].iterkeys():
    # iteraton on the keys to get the differents names in the table
        entree = KpiRedmine()
        entree.date = date
        entree.requests_opened = result_redmine['requests_opened'][date]
        entree.requests_closed = result_redmine['requests_closed'][date]
        entree.requests_remained = result_redmine['requests_remained'][date]
        entree.requests_lifetime = result_redmine['requests_lifetime'][date]
        entree.requests_lifetime_normal = \
            result_redmine['requests_lifetime_normal'][date]
        entree.requests_lifetime_high  = \
            result_redmine['requests_lifetime_high'][date]
        entree.requests_lifetime_urgent = \
            result_redmine['requests_lifetime_urgent'][date]
        entree.save()
        number += 1
        print "\r %s kpi redmine saved" % number,
    return number

def insert_nagios_notifications(notifications_nagios):
    """
    insert nagios notifications into the programm database
    """
    number = 0
    for notifications in notifications_nagios:
        entree = NagiosNotifications()
        entree.host = notifications[0]
        entree.service = notifications[1]
        entree.date = datetime.fromtimestamp(notifications[2], tz=utc)
        entree.state = notifications[3]

        if "ACKNOWLEDGEMENT" in notifications[4]:
            entree.acknowledged = True
        else:
            entree.acknowledged = False
        number += 1
        print "\r %s notifications saved" % number,
        entree.save()
    return number

def insert_nagios(result_nagios):
    """
    insert nagios kpi into the programm database
    """
    number = 0
    one_day = timedelta(days = 1)
    nagios_r = KpiNagios()
    nagios_r.date = datetime.now(tz=utc).replace(hour = 0,
        minute = 0, second = 0, microsecond = 0)-one_day


    # Nagios results ----------------------------------------------------------
    try:
        nagios_r.total_host = result_nagios['total_hosts']
        nagios_r.total_services = result_nagios['total_services']
        nagios_r.written_procedures = result_nagios['written_procedures']
        nagios_r.missing_procedures = result_nagios['missing_procedures']
        nagios_r.linux = result_nagios['linux']
        nagios_r.windows = result_nagios['windows']
        nagios_r.aix = result_nagios['aix']

        nagios_r.save()
        number += 1
        print "\n1 kpi nagios saved"
    except:
        pass
    return number

def insert_count_notifications():
    """
    insert the number of notifications for each state every day
    """
    print "\nCounting Nagios notifications"
    one_day = timedelta(days = 1)
    number = 0
    result = True
    if CountNotifications.objects.all().count() == 0:
        first_date = NagiosNotifications.objects.order_by('date')[0].date
    else:
        first_date = CountNotifications.objects.order_by('-date')[0].date
    first_date = first_date\
        .replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    result = nagios_notifications.request(first_date)
    while result != False:
        notif = CountNotifications()
        notif.date = first_date
        notif.warning = result['warning']
        notif.warning_acknowledged = result['warning_acknowledged']
        notif.critical = result['critical']
        notif.critical_acknowledged = result['critical_acknowledged']
        notif.save()
        first_date += one_day
        number += 1
        print "\r %s kpi notifications count saved" % number,
        result = nagios_notifications.request(first_date)
    return number

if __name__ == '__main__':
    print(insert())
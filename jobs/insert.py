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
from kpi.models import NagiosNotifications
from kpi.models import KpiRedmine, KpiNagios
from django.utils.timezone import utc


def insert():
    """
    Execute the requests in the differents databases, then stock the result in the programm database
    """

    # Stock the notifications from Nagios database in the program database ----

    result_nagios = get_result_nagios()
    notifications_nagios = get_notifications()

    number = 0

    number += insert_nagios_notifications(notifications_nagios)

    # Calculating from NagiosNotifications ------------------------------------

    number += insert_nagios(result_nagios)


    # Redmine results -----------------------------

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
        print "\n1 kpi nagios saved\n"
    except:
        pass
    return number

if __name__ == '__main__':
    print(insert())
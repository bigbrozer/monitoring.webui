"""
get the redmine kpi from redmine
"""

from django.conf import settings
import sqlite3
from apps.kpi.models import KpiRedmine
from datetime import datetime, timedelta
from django.utils.timezone import utc
import os

def request():
    """
    return the key indicators from redmine database
    """

    db_file = "/var/lib/dbconfig-common/sqlite3/redmine/instances/default/redmine_default" if not settings.DEVEL else os.path.join(settings.PROJECT_PATH, 'var/redmine_default')
    conn = sqlite3.connect(
        db_file, detect_types = sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()

    # count the number of entry in the programm database for the Redmine kpi
    number = KpiRedmine.objects.count()

    requests_opened = {}
    requests_closed = {}
    requests_remained = {}
    requests_lifetime_low = {}
    requests_lifetime_normal = {}
    requests_lifetime_high = {}
    requests_lifetime_urgent = {}
    requests_waiting = {}
    one_day = timedelta(days = 1)
    #frequency of execution
    today = datetime.now(tz=utc)
    today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    # first execution of the script
    if not number:
        cur.execute(
            "SELECT created_on FROM ISSUES ORDER BY created_on ASC LIMIT 1")
        day_midnight = cur.fetchone()[0]
        day_midnight -= one_day

        nrest = 0
    else:
        day_midnight = KpiRedmine.objects.order_by('-date')[0].date
        day_midnight += one_day


    day_midnight = day_midnight.replace(
        hour = 0, minute = 0, second = 0, microsecond = 0, tzinfo = utc)
    # first date found in redmine database
    day_late = day_midnight + one_day

    while day_late <= today:
    # loop that goes throuh all the database day per day
        date_midnight = day_midnight.date()
        tu1 = (day_midnight, day_late)
        tu2 = (day_late, day_midnight)
        cur.execute("SELECT COUNT (status_id) FROM ISSUES\
            WHERE created_on >= ? AND created_on < ? AND project_id != 12", tu1)
        requests_opened[str(day_midnight)] = cur.fetchone()[0]
        cur.execute("SELECT COUNT (status_id) FROM ISSUES\
            WHERE due_date = ? \
            AND (status_id = 5 OR status_id = 6 OR status_id = 10) AND project_id != 12", (date_midnight,))
        requests_closed[str(day_midnight)] = cur.fetchone()[0]
#        nrest = nrest + requests_opened[str(day_midnight)] - requests_closed[str(day_midnight)]
        avg = timedelta(days = 6*30)
        lifetime_low = timedelta()
        lifetime_normal = timedelta()
        lifetime_high = timedelta()
        lifetime_urgent = timedelta()
        num = 0
        n_low = 0
        n_normal = 0
        n_high = 0
        n_urgent = 0
#        cur.execute("Select count(status_id) from issues Where created_on < ? AND project_id != 12", (day_late,))
#        num1 = cur.fetchone()[0]
#        cur.execute("Select count(status_id) from issues Where due_date <= ? "\
#            "And (status_id = 5 OR status_id = 6 OR status_id = 10) AND project_id != 12", (day_midnight,))
#        num2 = cur.fetchone()[0]
#        num = num1 - num2
        cur.execute("SELECT count(id) FROM ISSUES "
                                    "WHERE created_on < ? "
                                    "AND (due_date > ? "
                                    "OR (status_id != 5 AND status_id != 6)) "
                                    "AND project_id != 12", tu2)
        requests_remained[str(day_midnight)] = cur.fetchone()[0]

#            num += 1
#            if requests[2] != '6' or requests[2] != '10':
#                if requests[1] == 3:
#                    lifetime += timedelta(days = (calcul_days(day_late, requests[0])))
#                    n_low += 1
#                if requests[1] == 4:
#                    lifetime_normal += timedelta(days = (calcul_days(day_late, requests[0])))
#                    n_normal += 1
#                elif requests[1] == 5:
#                    lifetime_high += timedelta(days = (calcul_days(day_late, requests[0])))
#                    n_high += 1
#                    #print all request that are here for more than 125 days
#                    # if day_late - requests[0].total_seconds() > 125*24*60*60:
#                    #     print "id : %s, subject : %s, cree : %s, status : %s"\
#                    #   % (requests[3], requests[4], requests[0], requests[2])
#                elif requests[1] == 6 or requests[1] == 7:
#                    lifetime_urgent += timedelta(days = (calcul_days(day_late, requests[0])))
#                    #print all request that are here for more than 75 days
#                    #if day_late - request[0].total_seconds() > 75*24*60*60:
#                    #    print "id : %s, subject : %s, cree : %s"\
#                    # % (request[3], request[4], request[0])
#
#                    n_urgent += 1
#        requests_remained[str(day_midnight)] = num
#        if num > 0:
#            requests_lifetime[str(day_midnight)] = \
#            (lifetime.total_seconds()/n_low)
#        else:
#            requests_lifetime[str(day_midnight)] = 0
#        if n_normal > 0:
#            requests_lifetime_normal[str(day_midnight)] = \
#            (lifetime_normal.total_seconds()/n_normal)
#        else:
#            requests_lifetime_normal[str(day_midnight)] = 0
#        if n_high > 0:
#            requests_lifetime_high[str(day_midnight)] = \
#            (lifetime_high.total_seconds()/n_high)
#        else:
#            requests_lifetime_high[str(day_midnight)] = 0
#        if n_urgent > 0:
#            requests_lifetime_urgent[str(day_midnight)] = \
#            (lifetime_urgent.total_seconds()/n_urgent)
#        else:
#            requests_lifetime_urgent[str(day_midnight)] = 0
        for request in cur.execute("SELECT created_on, due_date, priority_id FROM issues "
                                   "WHERE status_id = 5 "
                                   "AND due_date > ? "
                                   "AND due_date < ? "
                                   "AND project_id != 12", (day_midnight-avg, day_midnight)):
#        for request in cur.execute("SELECT created_on, due_date, priority_id FROM ISSUES "
#        "WHERE created_on < ? "
#        "AND (due_date > ? "
#        "OR (status_id != 5 AND status_id != 6 AND status_id != 10)) "
#        "AND project_id != 12", tu2):
            created_on = datetime.strptime(request[0], "%Y-%m-%d %H:%M:%S").date()

            if request[2] == 3:
                lifetime_low += request[1] - created_on
                n_low += 1
            elif request[2] == 4:
                lifetime_normal += request[1] - created_on
                n_normal += 1
            elif request[2] == 5:
                lifetime_high += request[1] - created_on
                n_high += 1
            elif request[2] >= 6:
                lifetime_urgent += request[1] - created_on
                n_urgent += 1
        if n_low > 0:
            requests_lifetime_low[str(day_midnight)] = (lifetime_low.total_seconds()/n_low)
        else:
            requests_lifetime_low[str(day_midnight)] = 0
        if n_normal > 0:
            requests_lifetime_normal[str(day_midnight)] = (lifetime_normal.total_seconds()/n_normal)
        else:
            requests_lifetime_normal[str(day_midnight)] = 0
        if n_high > 0:
            requests_lifetime_high[str(day_midnight)] = (lifetime_high.total_seconds()/n_high)
        else:
            requests_lifetime_high[str(day_midnight)] = 0
        if n_urgent > 0:
            requests_lifetime_urgent[str(day_midnight)] = (lifetime_urgent.total_seconds()/n_urgent)
        else:
            requests_lifetime_urgent[str(day_midnight)] = 0
        if n_normal + n_high + n_urgent != 0:
            requests_lifetime_low[str(day_midnight)] = (lifetime_normal.total_seconds() \
                                                        + lifetime_high.total_seconds() \
                                                        + lifetime_urgent.total_seconds()) / (n_normal + n_high + n_urgent)
        else:
            requests_lifetime_normal[str(day_midnight)] = 0


        if day_late == today:
            cur.execute("SELECT COUNT(id) FROM issues WHERE (status_id = 4 OR status_id = 9)"
                        "AND project_id != 12")
            requests_waiting[str(day_midnight)] = cur.fetchone()[0]
        else:
            requests_waiting[str(day_midnight)] = 0

        day_midnight += one_day
        day_late += one_day

    conn.close()

    results = {
    'requests_opened': requests_opened,
    'requests_closed': requests_closed,
    'requests_remained': requests_remained,
    'requests_lifetime_low': requests_lifetime_low,
    'requests_lifetime_normal': requests_lifetime_normal,
    'requests_lifetime_high': requests_lifetime_high,
    'requests_lifetime_urgent': requests_lifetime_urgent,
    'requests_waiting': requests_waiting
    }

    return results

def calcul_days(today, date_request):
    """
    calcul the number of days between two dates without the weekends
    """
    num = 0
    one_day = timedelta(days = 1)
    while date_request <  today:
        if date_request.weekday() != 5 and date_request.weekday() != 6:
            num += 1
        date_request += one_day
    return num

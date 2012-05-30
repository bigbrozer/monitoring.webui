import sqlite3
from kpi.models import KpiRedmine
from datetime import datetime, date, timedelta
from django.utils.timezone import utc

def request():
    """
    return the key indicators from redmine database
    """
    
    conn = sqlite3.connect("/home/fellet/redmine_default", detect_types = sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # count the number of entry in the programm database for the Redmine kpi
    number = KpiRedmine.objects.count()

    # first execution of the script
    if number == 0:
        c.execute("SELECT updated_on FROM ISSUES ORDER BY updated_on ASC LIMIT 1")
        first_date = c.fetchone()[0]
        first_date.replace(tzinfo = utc)
        #first_date = datetime.strptime(first_date, "%Y-%m-%d %H:%M:%S")
        # first date found in redmine database

        t = timedelta(days=1)
        #frequency of execution

        next_date = first_date + t
        today = datetime.now(tz=utc)
        requests_opened = {}
        requests_closed = {}
        requests_remained = {}
        requests_lifetime = {}
        print first_date
        while next_date < today: 
        # loop that goes throuh all the database day per day
            tu = (first_date, next_date)
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on > ? AND created_on < ?", tu)
            requests_opened[str(next_date)] = c.fetchone()[0]
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE status_id = 5 AND updated_on > ? AND updated_on < ?", tu)
            requests_closed[str(next_date)] = c.fetchone()[0]
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on < ? AND updated_on > ?", tu)
            requests_remained[str(next_date)] = c.fetchone()[0]
            lifetime = timedelta(days = 0)
            n = 0
            for request in c.execute('SELECT created_on, updated_on FROM ISSUES WHERE status_id = 5 AND updated_on > ? AND updated_on < ?', tu):
                lifetime += (request[1] - request[0])
                n += 1
            requests_lifetime[str(next_date)] = (lifetime/n)
            next_date += t
            first_date += t

    # at least the second execution        
    else:
        last_date = KpiRedmine.objects.order_by('-date')[0].date
        # last date found in the programm database
        tu = (last_date,)
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on > ?", tu)
        requests_opened[str(last_date)] = c.fetchone()[0]
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE status_id = 5 AND updated_on > ?", tu)
        requests_closed[str(last_date)] = c.fetchone()[0]
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on < ? AND status_id != 5 AND status_id != 6", tu)
        requests_remained[str(last_date)] = c.fetchone()[0]
        lifetime = timedelta(days = 0)
        n = 0
        for request in c.execute("SELECT (created_on, updated_on) FROM ISSUES WHERE status_id = 5 AND updated_on > ?", tu):
            lifetime += (request[1] - request[0])
            n += 1
        requests_lifetime[str(last_date)] = (lifetime/n)

    conn.close()

    results = {
    'requests_opened': requests_opened,
    'requests_closed': requests_closed,
    'requests_remained': requests_remained,
    'requests_lifetime': requests_lifetime
    }

    return results
	
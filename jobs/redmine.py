import sqlite3
from kpi.models import KpiRedmine
from datetime import datetime, date, timedelta
from django.utils.timezone import utc
from pprint import pprint

def request():
    """
    return the key indicators from redmine database
    """
    
    conn = sqlite3.connect("/home/fellet/redmine_default", detect_types = sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # count the number of entry in the programm database for the Redmine kpi
    number = KpiRedmine.objects.count()

    requests_opened = {}
    requests_closed = {}
    requests_remained = {}
    requests_lifetime = {}
    journey = timedelta(hours = 23, minutes = 59, seconds = 59)
    oneDay = timedelta(days = 1)
    #frequency of execution
    today = datetime.now(tz=utc)
    today = today.replace(hour = 0, minute = 0, second = 0)    

    # first execution of the script
    if number == 0:
        c.execute("SELECT updated_on FROM ISSUES ORDER BY updated_on ASC LIMIT 1")
        day_midnight = c.fetchone()[0]


        day_midnight = day_midnight.replace(hour = 0, minute = 0, second = 0, tzinfo = utc)
        # first date found in redmine database

        day_late = day_midnight + journey
                
        print day_midnight
        while day_midnight < today: 
        # loop that goes throuh all the database day per day
            tu = (day_midnight, day_late)
            tu2 = (day_late, day_late)
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on >= ? AND created_on < ?", tu)
            requests_opened[str(day_midnight)] = c.fetchone()[0]            
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE updated_on >= ? AND updated_on < ? AND (status_id = 5 OR status_id = 6 OR status_id = 10)", tu)
            requests_closed[str(day_midnight)] = c.fetchone()[0]            
            c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on <= ? AND (updated_on > ? OR (status_id != 5 AND status_id != 6 AND status_id != 10))", tu2)
            requests_remained[str(day_midnight)] = c.fetchone()[0]            
            lifetime = timedelta(days = 0)
            n = 0
            for request in c.execute('SELECT created_on, updated_on FROM ISSUES WHERE status_id = 5 AND updated_on > ? AND updated_on < ?', tu):
                lifetime += (request[1] - request[0])
                n += 1
            if n > 0:
                requests_lifetime[str(day_midnight)] = (lifetime.total_seconds()/n)
            else:
                requests_lifetime[str(day_midnight)] = 0
            day_midnight += oneDay
            day_late = day_midnight + journey

    # at least the second execution        
    else:
        day_midnight = KpiRedmine.objects.order_by('-date')[0].date
        # last date found in the programm database        
        tu = (day_midnight,)
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on > ?", tu)
        requests_opened[str(today)] = c.fetchone()[0]
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE status_id = 5 AND updated_on > ?", tu)
        requests_closed[str(today)] = c.fetchone()[0]
        c.execute("SELECT COUNT (status_id) FROM ISSUES WHERE created_on < ? AND status_id != 5 AND status_id != 6 AND status_id != 10", tu)
        requests_remained[str(today)] = c.fetchone()[0]
        lifetime = timedelta(days = 0)
        n = 0
        for request in c.execute("SELECT created_on, updated_on FROM ISSUES WHERE status_id = 5 AND updated_on > ?", tu):
            lifetime += (request[1] - request[0])
            n += 1
        if n > 0:
            requests_lifetime[str(today)] = (lifetime/n)
        else:
            requests_lifetime[str(today)] = 0

    conn.close()

    results = {
    'requests_opened': requests_opened,
    'requests_closed': requests_closed,
    'requests_remained': requests_remained,
    'requests_lifetime': requests_lifetime
    }

    return results
	
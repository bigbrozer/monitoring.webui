import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(sys.argv[0])))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reporting.settings'

import nagios
import nagios_notifications
import redmine
from pprint import pprint
from kpi.models import NagiosNotifications
from kpi.models import KpiRedmine, KpiNagios
from django.utils.timezone import utc


def collecte():
    """
    Execute the requests in the differents databases, then stock the result in the programm database
    """

    # Stock the notifications from Nagios database in the program database ----

    lastTimestamp = nagios_notifications.getLastTime()
    
    resultNagios = nagios.request(lastTimestamp)  
    number = 0 

    for notifications in resultNagios['notifications']:
        entree = NagiosNotifications()
        entree.host = notifications[0]
        entree.service = notifications[1]        
        entree.date = datetime.fromtimestamp(notifications[2], tz=utc)    
        entree.state = notifications[3]
        if "ACKNOWLEDGEMENT" in notifications[4]:
            entree.acknowledged = True
        else:
            entree.acknowledged = False
        number +=1
        print "\r %s notifications saved" % number,
        entree.save()
    print "\n"
        

    # End ---------------------------------------------------------------------

    # Calculating from NagiosNotifications ------------------------------------

    resultNagiosNotifications = nagios_notifications.request()

    nagiosR = KpiNagios()
    nagiosR.date = datetime.now(tz=utc)
    
    # Nagios results ----------------------------------------------------------
    nagiosR.total_host = resultNagios['total_hosts']
    nagiosR.total_services = resultNagios['total_services']
    nagiosR.written_procedures = 1
    nagiosR.missing_procedures = 1
    nagiosR.linux = resultNagios['linux']
    nagiosR.windows = resultNagios['windows']
    nagiosR.aix = resultNagios['aix']

    # NagiosNotifications results -----------------
    nagiosR.alerts_hard_warning = resultNagiosNotifications['alerts_hard_warning']
    nagiosR.alerts_hard_critical = resultNagiosNotifications['alerts_hard_critical']
    nagiosR.alerts_acknowledged_warning = resultNagiosNotifications['alerts_acknowledged_warning']
    nagiosR.alerts_acknowledged_critical = resultNagiosNotifications['alerts_acknowledged_critical']

    # Redmine results -----------------------------
    resultRedmine = redmine.request()
    numberR = 0
    for dateR in resultRedmine['requests_opened'].iterkeys():
        entreeR = KpiRedmine()
        entreeR.date = dateR
        entreeR.requests_opened = resultRedmine['requests_opened'][dateR]
        entreeR.requests_closed = resultRedmine['requests_closed'][dateR]
        entreeR.requests_remained = resultRedmine['requests_remained'][dateR]
        entreeR.requests_lifetime = resultRedmine['requests_lifetime'][dateR]
        entreeR.save()
        numberR += 1
        print "\r %s entrees sauvees (kpi redmine)" % numberR,
        
    nagiosR.save()
    return "\n %s lignes ajoutees et 13/15 kpi aussi" % (number+numberR)
#resultRedmine = requestRedmine()

if __name__ == '__main__':
    r = collecte()
    print(r)
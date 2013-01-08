"""
get the results from nagios
"""

from django.conf import settings
from apps.nagios.models import Satellite
import os
from os import path


SATELLITES = Satellite.live_connect()

def request():
    """
    get the kpi from redmine
    """
    kbpath = "/var/www/kb/data/pages" if not settings.DEVEL else os.path.join(settings.PROJECT_PATH, 'var/pages')

    if not SATELLITES:
        return False

    print "Fetching informations for the kpi nagios"

    # Total number of hosts ---------------------------------------------------

    nb_total_hosts = SATELLITES.query("""\
GET hosts
Stats: name != \" \"
""")
    nombre = 0
    for sat in nb_total_hosts:
        nombre += sat[0]

    nb_total_hosts = nombre


    # Total number of services ------------------------------------------------

    nb_total_services = SATELLITES.query("""\
GET services
Stats: description != \" \"
""")
    nombre = 0
    for sat in nb_total_services:
        nombre += sat[0]

    nb_total_services = nombre


    # Total number of Linux ---------------------------------------------------

    nb_linux = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_linux
""")
    nombre = 0
    for sat in nb_linux:
        nombre += sat[0]

    nb_linux = nombre


    # Total number of Windows -------------------------------------------------

    nb_windows = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_windows
""")
    nombre = 0
    for sat in nb_windows:
        nombre += sat[0]

    nb_windows = nombre


    # Total number of AIX -----------------------------------------------------

    nb_aix = SATELLITES.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_aix
""")
    nombre = 0
    for sat in nb_aix:
        nombre += sat[0]

    nb_aix = nombre

    # get the service with path to the procedure ------------------------------

    services_all = SATELLITES.query("""\
GET services
Columns: host_name description notes_url_expanded contact_groups
""")
    written_procedures = 0
    missing_procedures = 0
    total_written = 0
    total_missing = 0

    csv_report_dir = "/home/django/public_html/reporting" if not settings.DEVEL else "/tmp"

    myreport = open(path.join(csv_report_dir, "detailled_report.csv"), "w")
    my_simple_report = open(path.join(csv_report_dir, "simple_report.csv"), "w")
    myreport.write("written;hostname;services;procedure;stratos\n")
    my_simple_report.write("written;procedure;\n")
    procedures = {}
    for services in services_all:
        procedure_path = services[2].split('/')[-1].strip(':').replace(':', '/').lower()
        empty = 1
        for serv in services[3]:
            if empty == 1:
                list_contact = "%s" % serv
                empty = 0
            else:
                list_contact += ", %s" % serv
                empty = 0
        if path.lexists("%s/%s.txt" % (kbpath, procedure_path)):
            total_written +=1
            myreport.write("yes;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 1
        else:
            total_missing += 1
            myreport.write("no;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 0
    for procedure, written in procedures.items():
        if written:
            my_simple_report.write("yes;%s\n" % procedure)
            written_procedures += 1
        else:
            my_simple_report.write("no;%s\n" % procedure)
            missing_procedures += 1
    myreport.close()

    result = {
    'total_hosts': nb_total_hosts,
    'total_services': nb_total_services,
    'linux': nb_linux,
    'windows': nb_windows,
    'aix': nb_aix,
    'written_procedures': written_procedures,
    'missing_procedures': missing_procedures,
    'total_written' : total_written,
    'total_missing' : total_missing
    }

    return result

def request_notifications(last_timestamp):
    """
    get the notifications from nagios
    """
    print "Fetching informations for the nagios notifications"
    # Get ALL the notifications from the last timestamp -----------------------

    notifications_satellites = SATELLITES.query("""\
GET log
Columns: host_name service_description time state options
Filter: class = 3
Filter: time > %s
Filter: command_name ~ email
Filter: options !~ ACKNOWLEDGEMENT
Filter: state = 1
And: 2
Filter: options !~ ACKNOWLEDGEMENT
Filter: state = 2
And: 2
Filter: options ~ ACKNOWLEDGEMENT
Filter: state = 1
And: 2
Filter: options ~ ACKNOWLEDGEMENT
Filter: state = 2
And: 2
Or: 4
""" % last_timestamp)

    return notifications_satellites

def request_oldest_alerts_hosts():
    """
    return a dictionnary containing the oldest active alerts
    """
    oldest_alerts = SATELLITES.query("""\
GET hosts
Columns: name last_hard_state_change
Filter: hard_state = 1
Filter: state > 0
""")
    return oldest_alerts

def request_oldest_alerts_services():
    """
    return a dictionnary containing the oldest active alerts
    """
    oldest_alerts = SATELLITES.query("""\
GET services
Columns: host_name description last_hard_state_change
Filter: state_type = 1
Filter: state = 1
Filter: state = 2
Or: 2
""")
    return oldest_alerts








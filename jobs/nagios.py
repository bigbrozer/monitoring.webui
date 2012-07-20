"""
get the results from nagios
"""

import livestatus as live
from os import path


def get_satellites():
    """
    return the key indicators from the last timestamp to now
    """

    connections = {
        'EDC1': {
            'alias': 'nagios.edc.eu.corp',
            'socket': 'tcp:10.20.104.113:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'EDC2': {
            'alias': 'nagios-2.edc.eu.corp',
            'socket': 'tcp:10.20.104.114:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'ADC': {
            'alias': 'nagios.cn.corp',
            'socket': 'tcp:10.167.0.245:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'MOP': {
            'alias': 'nagios.mop.fr.corp',
            'socket': 'tcp:10.51.194.220:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'IDC': {
            'alias': 'nagios.idc.us.corp',
            'socket': 'tcp:10.135.0.7:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'HGB2': {
            'alias': 'nagios-2.eas.ww.corp',
            'socket': 'tcp:10.20.178.8:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'HGB': {
            'alias': 'nagios.eas.ww.corp',
            'socket': 'tcp:10.20.178.7:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },
        'EDC3': {
            'alias': 'nagios-3.edc.eu.corp',
            'socket': 'tcp:10.20.104.208:6557',
            'nagios_url': '/nagios',
            'timeout': 5,
        },

    }

    print "connection in progress"
    for i in range(0, 2):
        satellites = live.MultiSiteConnection(connections)
        if not satellites.dead_sites():
            print "connection initialized"
            return satellites

    return False

SATELLITES = get_satellites()

def request():
    """
    get the kpi from redmine
    """
    kbpath = "/tmp/pages"

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
    myreport = open("kpi/static/detailled_report.csv", "w")
    my_simple_report = open("kpi/static/simple_report.csv", "w")
    myreport.write("written;hostname;services;procedure;stratos\n")
    my_simple_report.write("written;procedure;\n")
    procedures = {}
    for services in services_all:
        procedure_path = services[2].split('/')[-1].replace(':', '/').lower()
        empty = 1
        for serv in services[3]:
            if empty == 1:
                list_contact = "%s" % serv
                empty = 0
            else:
                list_contact += ", %s" % serv
                empty = 0
        if path.lexists("%s/%s.txt" % (kbpath, procedure_path)):
            written_procedures += 1
            myreport.write("yes;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 1
        else:
            missing_procedures += 1
            myreport.write("no;%s;%s;%s;%s\n" % (services[0],
                services[1], services[2], list_contact))
            procedures[str(services[2])] = 0
    for procedure, written in procedures.items():
        if written:
            my_simple_report.write("yes;%s\n" % procedure)
        else:
            my_simple_report.write("no;%s\n" % procedure)
    myreport.close()

    result = {
    'total_hosts': nb_total_hosts,
    'total_services': nb_total_services,
    'linux': nb_linux,
    'windows': nb_windows,
    'aix': nb_aix,
    'written_procedures': written_procedures,
    'missing_procedures': missing_procedures
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

def get_hosts():
    """
    get the hosts from nagios
    """
    print "\nFetching informations for the hosts"
    hosts = SATELLITES.query("""\
GET hosts
Column: name
""")
    return hosts

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








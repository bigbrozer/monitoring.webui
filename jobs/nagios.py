import livestatus as live

def request(lastTimestamp):
    """
    return the key indicators from the last timestamp to now 
    param lastTimestamp: the last timestamp found in the database
    type lastTimestamp: integer 

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
    satellites = live.MultiSiteConnection(connections)


    # Total number of hosts ---------------------------------------------------

    nb_total_hosts = satellites.query("""\
GET hosts
Stats: name != \" \"
""")
    nombre = 0
    for sat in nb_total_hosts:
        nombre += sat[0]

    nb_total_hosts = nombre


    # Total number of services ------------------------------------------------

    nb_total_services = satellites.query("""\
GET services
Stats: description != \" \"
""")
    nombre = 0
    for sat in nb_total_services:
        nombre += sat[0]

    nb_total_services = nombre


    # Total number of Linux ---------------------------------------------------

    nb_linux = satellites.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_linux
""")
    nombre = 0
    for sat in nb_linux:
        nombre += sat[0]

    nb_linux = nombre


    # Total number of Windows -------------------------------------------------

    nb_windows = satellites.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_windows
""")
    nombre = 0
    for sat in nb_windows:
        nombre += sat[0]

    nb_windows = nombre


    # Total number of AIX -----------------------------------------------------

    nb_aix = satellites.query("""\
GET hostgroups
Columns: num_hosts
Filter: name = sys_aix
""")    
    nombre = 0
    for sat in nb_aix:
        nombre += sat[0]

    nb_aix = nombre
    

    # Get ALL the notifications from the last timestamp -----------------------

    notifications_satellites = satellites.query("""\
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
""" % lastTimestamp)


    result = {
    'total_hosts': nb_total_hosts,
    'total_services': nb_total_services,
    'linux': nb_linux,
    'windows': nb_windows,
    'aix': nb_aix,
    'notifications' : notifications_satellites
    }

    return result
    

